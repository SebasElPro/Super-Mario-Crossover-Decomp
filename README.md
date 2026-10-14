# SMBC4 en Android (Python + Kivy)

1. Copia dentro de `game/` estos elementos de tu zip `SMBC4/`:
   - `Build/`
   - `TemplateData/`
   - `Index.html`
   (HFS.exe y SMBC4.VFS no hacen falta.)
2. Compila (Linux o WSL2, con Python 3 y Buildozer):
   ```
   pip install buildozer cython
   buildozer android debug
   ```
3. El APK queda en `bin/`. Instálalo con `buildozer android deploy run`
   o copiándolo al móvil.

Probar en PC: `pip install kivy` y `python main.py` (abre el navegador).

Notas
- El servidor local de Python (127.0.0.1:8765) sirve el juego al WebView.
- Si el juego usa otras teclas, edita `KEYMAP` en `touch_controls.js`.
- Si falla `usesCleartextTraffic`, revisa la opción
  `android.extra_manifest_application_arguments` según tu versión de Buildozer.
- Es un juego de terceros (Exploding Rabbit / personajes de Nintendo):
  úsalo de forma personal, no lo redistribuyas.

## Compilar sin Linux (GitHub Actions)
1. Crea un repositorio en GitHub y sube TODO este proyecto (incluida la carpeta
   `.github` y `game/` con la build). Usa GitHub Desktop: la web limita a 25 MB
   por archivo y los de `game/Build` pesan ~50 MB.
2. En GitHub: pestaña Actions -> "Build APK" -> Run workflow.
3. Al terminar (20-40 min), descarga `smbc4-apk` desde el resumen de la ejecución.
