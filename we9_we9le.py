#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convertidor de option files  WE9 <-> WE9LE (Liveware Evolution), PC.

Uso:  arrastra uno o varios option files sobre este programa (o sobre el .bat).
      Por cada archivo genera DOS versiones, listas para copiar a la carpeta de saves:
         <carpeta del archivo>\\convertido_<nombre>\\WE9\\KONAMI-WIN32WE9UOPT     (WE9 regular)
         <carpeta del archivo>\\convertido_<nombre>\\WE9LE\\KONAMI-WIN32WE9KOPT   (WE9LE)
      La version que ya coincide con la del archivo de entrada se copia sin cambios.

Como funciona: los dos juegos usan el mismo formato y el mismo cifrado. Solo cambian los
primeros 9500 bytes (cabecera y bloques de ajustes del sistema). Se sustituyen por los de la
version de destino y se comprueban los checksums de los 10 bloques. No se toca nada mas
(jugadores, equipos, plantillas, kits...). El archivo de entrada nunca se modifica.

Estado: WE9 -> WE9LE comprobado en el juego. WE9LE -> WE9 comprobado en estructura y checksums,
pero no probado todavia en el juego.
"""
import base64, os, struct, sys

LONGITUD = 1250304
PREFIJO = 9500
NOMBRE_REGULAR = "KONAMI-WIN32WE9UOPT"
NOMBRE_LE = "KONAMI-WIN32WE9KOPT"
BLOQUES = [12, 5144, 9508, 14044, 36872, 657712, 803608, 822940, 969192, 1228568]
TAMANOS = [4948, 1232, 4520, 22816, 620000, 145880, 19320, 146240, 259364, 21016]
CHECKSUMS_EN_PREFIJO = set(range(4, 8)) | set(range(5136, 5140))

KEYPC = bytes([115, 96, 225, 198, 31, 60, 173, 66, 11, 88, 185, 254, 55, 180, 5, 250, 163, 80, 145, 54, 79, 44, 93, 178, 59, 72, 105, 110, 103, 164, 181, 106, 211, 64, 65, 166, 127, 28, 13, 34, 107, 56, 25, 222, 151, 148, 101, 218, 3, 48, 241, 22, 175, 12, 189, 146, 155, 40, 201, 78, 199, 132, 21, 74, 51, 32, 161, 134, 223, 252, 109, 2, 203, 24, 121, 190, 247, 116, 197, 186, 99, 16, 81, 246, 15, 236, 29, 114, 251, 8, 41, 46, 39, 100, 117, 42, 147, 0, 1, 102, 63, 220, 205, 226, 43, 248, 217, 158, 87, 84, 37, 154, 195, 240, 177, 214, 111, 204, 125, 82, 91, 232, 137, 14, 135, 68, 213, 10, 243, 224, 97, 70, 159, 188, 45, 194, 139, 216, 57, 126, 183, 52, 133, 122, 35, 208, 17, 182, 207, 172, 221, 50, 187, 200, 233, 238, 231, 36, 53, 234, 83, 192, 193, 38, 255, 156, 141, 162, 235, 184, 153, 94, 23, 20, 229, 90, 131, 176, 113, 150, 47, 140, 61, 18, 27, 168, 73, 206, 71, 4, 149, 202, 179, 160, 33, 6, 95, 124, 237, 130, 75, 152, 249, 62, 119, 244, 69, 58, 227, 144, 209, 118, 143, 108, 157, 242, 123, 136, 169, 174, 167, 228, 245, 170, 19, 128, 129, 230, 191, 92, 77, 98, 171, 120, 89, 30, 215, 212, 165, 26, 67, 112, 49, 86, 239, 76, 253, 210, 219, 104, 9, 142, 7, 196, 85, 138])

_PLANTILLA_REGULAR = """
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
"""
_PLANTILLA_LE = """
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
"""
PLANTILLA = {
    "regular": base64.b64decode("".join(_PLANTILLA_REGULAR.split())),
    "le": base64.b64decode("".join(_PLANTILLA_LE.split())),
}
assert len(PLANTILLA["regular"]) == PREFIJO and len(PLANTILLA["le"]) == PREFIJO
ETIQUETA = {"regular": "WE9 (regular)", "le": "WE9LE (Liveware Evolution)"}
CARPETA = {"regular": "WE9", "le": "WE9LE"}
NOMBRE = {"regular": NOMBRE_REGULAR, "le": NOMBRE_LE}


def deshacer_xor(datos):
    return bytearray(b ^ KEYPC[i & 255] for i, b in enumerate(datos))


def checksums_validos(datos):
    """Comprueba el checksum de los 10 bloques (suma de palabras de 32 bits)."""
    buf = deshacer_xor(datos)
    malos = []
    for i in range(10):
        n = TAMANOS[i] // 4
        suma = sum(struct.unpack_from("<%dI" % n, buf, BLOQUES[i])) & 0xFFFFFFFF
        guardado = struct.unpack_from("<I", buf, BLOQUES[i] - 8)[0]
        if suma != guardado:
            malos.append(i)
    return malos


_DIF = [i for i in range(PREFIJO)
        if PLANTILLA["regular"][i] != PLANTILLA["le"][i] and i not in CHECKSUMS_EN_PREFIJO]


def detectar(datos, nombre_archivo):
    """Devuelve ('regular'|'le', motivo)."""
    pr = sum(1 for i in _DIF if datos[i] == PLANTILLA["regular"][i])
    pl = sum(1 for i in _DIF if datos[i] == PLANTILLA["le"][i])
    por_nombre = None
    n = nombre_archivo.upper()
    if n.endswith("WE9UOPT"):
        por_nombre = "regular"
    elif n.endswith("WE9KOPT") or n.endswith("WE9LEOPT"):
        por_nombre = "le"
    if pr != pl:
        v = "regular" if pr > pl else "le"
        return v, "por contenido (%d de %d marcas coinciden con %s)" % (max(pr, pl), len(_DIF), ETIQUETA[v])
    if por_nombre:
        return por_nombre, "por el nombre del archivo (el contenido no permite decidir)"
    return None, "no se pudo identificar la version"


def convertir(datos, destino):
    salida = bytearray(datos)
    salida[:PREFIJO] = PLANTILLA[destino]
    return bytes(salida)


def procesar(ruta, forzar=False):
    nombre = os.path.basename(ruta)
    print("=" * 66)
    print("Archivo:", ruta)
    with open(ruta, "rb") as f:
        datos = f.read()
    if len(datos) != LONGITUD:
        extra = ""
        if len(datos) == 1191936:
            extra = " (parece un option file de PES6, no de WE9)"
        print("ERROR: el tamano es %d bytes y deberia ser %d%s." % (len(datos), LONGITUD, extra))
        return False
    malos = checksums_validos(datos)
    if malos and not forzar:
        print("ERROR: los checksums de los bloques %s no coinciden. El archivo esta danado o no es un" % malos)
        print("       option file de WE9/WE9LE. (Usa --forzar para intentarlo igualmente.)")
        return False
    origen, motivo = detectar(datos, nombre)
    if origen is None:
        print("ERROR:", motivo, "- usa --regular o --le para indicar la version de origen.")
        return False
    print("Version detectada:", ETIQUETA[origen], "-", motivo)
    base = os.path.join(os.path.dirname(os.path.abspath(ruta)), "convertido_" + nombre)
    ok = True
    for dest in ("regular", "le"):
        res = datos if dest == origen else convertir(datos, dest)
        # verificaciones
        if len(res) != LONGITUD or checksums_validos(res):
            print("ERROR de verificacion en la salida", ETIQUETA[dest]); ok = False; continue
        if res[PREFIJO:] != datos[PREFIJO:] or (dest != origen and res[:PREFIJO] != PLANTILLA[dest]):
            print("ERROR de verificacion (bytes inesperados) en", ETIQUETA[dest]); ok = False; continue
        carpeta = os.path.join(base, CARPETA[dest])
        os.makedirs(carpeta, exist_ok=True)
        destino = os.path.join(carpeta, NOMBRE[dest])
        if os.path.abspath(destino) == os.path.abspath(ruta):
            print("ERROR: la salida coincide con el archivo de entrada."); ok = False; continue
        with open(destino, "wb") as f:
            f.write(res)
        print("  %-28s -> %s%s" % (ETIQUETA[dest], destino, "   (sin cambios)" if dest == origen else ""))
    if ok:
        print("Checksums verificados en las dos salidas. Copia la que corresponda a la carpeta de saves.")
    return ok


def main(argv):
    forzar = "--forzar" in argv
    pausa = "--no-pausa" not in argv
    archivos = [a for a in argv if not a.startswith("--")]
    if not archivos:
        print(__doc__)
        print("No se indico ningun archivo. Arrastra un option file sobre este programa.")
        resultado = False
    else:
        resultado = all([procesar(a, forzar) for a in archivos])
    if pausa:
        try:
            input("\nPulsa Enter para cerrar...")
        except EOFError:
            pass
    return 0 if resultado else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
