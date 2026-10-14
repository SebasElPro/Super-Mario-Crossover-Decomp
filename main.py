"""SMBC4 -> Android (Kivy + WebView).

Arranca un servidor HTTP local en Python que sirve la build Unity WebGL
(carpeta ./game) y la muestra en un WebView nativo a pantalla completa.
"""
import functools
import http.server
import os
import socketserver
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.utils import platform

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = os.path.join(BASE_DIR, "game")
TOUCH_JS = "touch_controls.js"


class GameHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".unityweb": "application/octet-stream",
        ".json": "application/json",
        ".js": "application/javascript",
    }

    def log_message(self, *args):
        pass

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/Index.html", "/index.html"):
            self._serve_index()
        elif path == "/" + TOUCH_JS:
            self._serve_file(os.path.join(BASE_DIR, TOUCH_JS), "application/javascript")
        else:
            super().do_GET()

    def _serve_file(self, filepath, ctype):
        with open(filepath, "rb") as f:
            data = f.read()
        self._send(data, ctype)

    def _serve_index(self):
        with open(os.path.join(GAME_DIR, "Index.html"), "rb") as f:
            html = f.read().decode("utf-8", "replace")
        tag = '<script src="/%s"></script></body>' % TOUCH_JS
        html = html.replace("</body>", tag) if "</body>" in html else html + tag
        self._send(html.encode("utf-8"), "text/html; charset=utf-8")

    def _send(self, data, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)


class ThreadedServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def start_server():
    handler = functools.partial(GameHandler, directory=GAME_DIR)
    server = ThreadedServer(("127.0.0.1", PORT), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def open_webview(url):
    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    WebView = autoclass("android.webkit.WebView")
    WebViewClient = autoclass("android.webkit.WebViewClient")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
    activity = PythonActivity.mActivity

    @run_on_ui_thread
    def create():
        wv = WebView(activity)
        s = wv.getSettings()
        s.setJavaScriptEnabled(True)
        s.setDomStorageEnabled(True)
        s.setMediaPlaybackRequiresUserGesture(False)
        s.setUseWideViewPort(True)
        s.setLoadWithOverviewMode(True)
        wv.setWebViewClient(WebViewClient())
        activity.addContentView(wv, LayoutParams(-1, -1))
        wv.loadUrl(url)

    create()


class SMBC4App(App):
    def build(self):
        return Widget()

    def on_start(self):
        if not os.path.isfile(os.path.join(GAME_DIR, "Index.html")):
            print("Falta la carpeta game/ con la build de Unity WebGL")
            return
        start_server()
        if platform == "android":
            Clock.schedule_once(
                lambda dt: open_webview("http://127.0.0.1:%d/" % PORT), 0.5
            )
        else:
            import webbrowser
            webbrowser.open("http://127.0.0.1:%d/" % PORT)  # prueba en PC

    def on_pause(self):
        return True


if __name__ == "__main__":
    SMBC4App().run()
