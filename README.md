# Convertidor de option files WE9 ⇄ WE9LE (PC)

Convierte un option file de **Winning Eleven 9** en uno de **WE9 Liveware Evolution** y al revés, para usar la misma base
de datos editada (jugadores, equipos, plantillas, kits) en los dos juegos.

Por cada archivo genera **las dos versiones**, listas para copiar a la carpeta de partidas. Nunca modifica el archivo
de entrada.

## Por qué hace falta

WE9 y WE9LE usan el **mismo formato y el mismo cifrado**: los jugadores, equipos y plantillas están en el mismo lugar. Lo
único que cambia son los **primeros 9500 bytes** (cabecera y bloques de ajustes del sistema). Si un option file tiene la
cabecera del otro juego, el juego lo rechaza. Un editor que guardó un WE9LE con cabecera de WE9 dejó un archivo
inservible, y de ahí salió esta herramienta.

## Uso

1. Arrastrá tu option file (`KONAMI-WIN32WE9UOPT` o `KONAMI-WIN32WE9KOPT`) sobre `arrastrar_aqui.bat`, o sobre
   `WE9_WE9LE_convertidor.exe` de **Releases**. Se pueden arrastrar varios a la vez.
2. Junto al archivo aparece `convertido_<nombre>\` con:

```
WE9\KONAMI-WIN32WE9UOPT      → para WE9
WE9LE\KONAMI-WIN32WE9KOPT    → para WE9 Liveware Evolution
```

   La versión que coincide con tu archivo es una copia sin cambios.
3. Hacé copia de tu option file actual y copiá el que corresponda a la carpeta de partidas del juego.

Por consola: `python we9_we9le.py ARCHIVO [ARCHIVO…] [--forzar] [--no-pausa]`.

## Cómo funciona

1. **Valida** el tamaño (1.250.304 bytes) y los checksums de los 10 bloques. Con `--forzar` lo intenta igual.
2. **Detecta la versión** comparando el contenido con las marcas que distinguen las dos cabeceras. Si el contenido no
   alcanza para decidir, usa el nombre del archivo (`…WE9UOPT` = WE9, `…WE9KOPT` = WE9LE).
3. **Reemplaza los primeros 9500 bytes** por la cabecera y los ajustes de la versión de destino. Las plantillas van
   embebidas en el script y salen de archivos reales de cada juego.
4. **Verifica** las dos salidas (checksums y que ningún byte fuera del prefijo haya cambiado) antes de darlas por buenas.

Formato completo del option file y diferencias entre juegos: repo **we-espia**, `docs/OPTION_FILES.md`.

## Estado

- **WE9 → WE9LE**: probado en el juego. Es idéntico byte a byte al archivo que se usó en la prueba.
- **WE9LE → WE9**: verificado en estructura y checksums, sin probar en el juego todavía.
- Los ajustes del sistema del archivo convertido (opciones del menú) pasan a ser los de la plantilla incluida.

## Compilar

Python 3, solo biblioteca estándar. Exe portable: `compilar_exe.bat` (PyInstaller, `WE9_WE9LE_convertidor.spec`). Algunos
antivirus marcan los exe de PyInstaller; es un falso positivo, y `arrastrar_aqui.bat` funciona sin compilar.

## Repos relacionados

- **Convertidor-PES5TOPES6**: pasa jugadores y plantillas de WE9/PES5/WE9LE a PES6.
- **we-espia**: lector en vivo de partidos y librería de option files.

## Licencia

MIT. Winning Eleven y KONAMI son marcas de Konami. Proyecto de fans, sin relación con Konami.
