// Controles táctiles: convierten toques en eventos de teclado para Unity WebGL.
// Ajusta KEYMAP si el juego usa otras teclas.
(function () {
  var KEYMAP = {
    left: 37, up: 38, right: 39, down: 40,
    a: 90,      // Z  (salto)
    b: 88,      // X  (correr / acción)
    start: 13   // Enter
  };

  // Pantalla completa
  var st = document.createElement("style");
  st.textContent =
    "html,body{margin:0;padding:0;background:#231F20;overflow:hidden;height:100%}" +
    ".webgl-content{position:fixed!important;left:0!important;top:0!important;" +
    "margin:0!important;transform:none!important;width:100%!important;height:100%!important}" +
    "#unityContainer{width:100%!important;height:100%!important}" +
    ".tc{position:fixed;z-index:9999;user-select:none;-webkit-user-select:none;touch-action:none}" +
    ".tc b{position:absolute;display:flex;align-items:center;justify-content:center;" +
    "width:64px;height:64px;border-radius:50%;background:rgba(255,255,255,.28);" +
    "color:#fff;font:bold 20px sans-serif;border:2px solid rgba(255,255,255,.5)}" +
    ".tc b.on{background:rgba(255,255,255,.6)}";
  document.head.appendChild(st);

  function key(type, code) {
    var e = new KeyboardEvent(type, { bubbles: true, cancelable: true });
    Object.defineProperty(e, "keyCode", { get: function () { return code; } });
    Object.defineProperty(e, "which", { get: function () { return code; } });
    document.dispatchEvent(e);
    window.dispatchEvent(e);
  }

  function pad(css, buttons) {
    var box = document.createElement("div");
    box.className = "tc";
    box.style.cssText = css;
    buttons.forEach(function (d) {
      var el = document.createElement("b");
      el.textContent = d.label;
      el.style.cssText = d.pos;
      var down = function (ev) { ev.preventDefault(); el.classList.add("on"); key("keydown", KEYMAP[d.k]); };
      var up = function (ev) { ev.preventDefault(); el.classList.remove("on"); key("keyup", KEYMAP[d.k]); };
      el.addEventListener("pointerdown", down);
      el.addEventListener("pointerup", up);
      el.addEventListener("pointercancel", up);
      el.addEventListener("pointerleave", up);
      box.appendChild(el);
    });
    document.body.appendChild(box);
  }

  function init() {
    pad("left:16px;bottom:16px;width:200px;height:200px", [
      { k: "up",    label: "▲", pos: "left:68px;top:0" },
      { k: "left",  label: "◀", pos: "left:0;top:68px" },
      { k: "right", label: "▶", pos: "left:136px;top:68px" },
      { k: "down",  label: "▼", pos: "left:68px;top:136px" }
    ]);
    pad("right:16px;bottom:16px;width:170px;height:150px", [
      { k: "b", label: "B", pos: "left:0;top:70px" },
      { k: "a", label: "A", pos: "left:100px;top:20px" }
    ]);
    pad("right:16px;top:12px;width:70px;height:40px", [
      { k: "start", label: "II", pos: "left:0;top:0;width:56px;height:36px;border-radius:12px" }
    ]);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
