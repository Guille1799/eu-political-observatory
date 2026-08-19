"""
Lector minimo de Word 97-2003 (.doc) en Python puro.

Por que existe este modulo
--------------------------
La especificacion del layout de los ficheros de Infoelectoral viaja DENTRO del
propio zip de descarga, en un `FICHEROS.doc` que es un binario OLE2 (Word 97).
La regla del proyecto es que el layout se LEE, no se supone -- asi que hay que
poder abrir ese .doc desde codigo.

En esta maquina habia un `antiword` instalado que lo extrae bien. No se usa, y el
motivo es el mismo que ya mordio con el certificado TLS (seccion 7-bis del
alcance): lo que funciona en la maquina de uno no es lo que funciona. Un binario
de mingw que no esta en Linux, ni en CI, ni en la maquina de quien replique esto
convierte un paso reproducible en un paso que solo sale aqui. Todo lo de abajo es
libreria estandar.

La salida de este modulo se contrasto con la de `antiword` mientras se escribia, y
coinciden. Pero esa comprobacion fue de quien lo escribio, no del repo. Lo que el
repo comprueba -- y es bastante mas fuerte -- es que el esquema que sale de aqui
encaja al byte con los .dat reales: ver `test_layout_infoelectoral.py`.

Alcance deliberado: extrae TEXTO, con las marcas de celda y de fila intactas, que
es lo unico que hace falta para leer tablas. No interpreta formato, ni imagenes,
ni campos, ni control de cambios.

Referencia del formato: [MS-CFB] (contenedor OLE2) y [MS-DOC] (FIB y piece table).
"""

from __future__ import annotations

import struct

FIRMA_OLE2 = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"

# Marcas de Word que sobreviven a la extraccion y que el parseador de tablas usa.
FIN_CELDA = "\x07"  # duplicada, cierra tambien la fila
FIN_PARRAFO = "\r"

# Cualquier valor >= a esto no es un sector valido (FREESECT, ENDOFCHAIN, ...).
_CADENA_LIBRE = 0xFFFFFFFA


class DocIlegible(Exception):
    """El fichero no es un .doc de Word 97-2003 legible por este modulo."""


class _ContenedorOle2:
    """Lo minimo del formato de fichero compuesto: sacar streams por nombre."""

    def __init__(self, datos):
        if datos[:8] != FIRMA_OLE2:
            raise DocIlegible("no empieza por la firma OLE2")
        self._d = datos
        self._tam_sector = 1 << struct.unpack_from("<H", datos, 30)[0]
        self._tam_mini = 1 << struct.unpack_from("<H", datos, 32)[0]
        n_fat = struct.unpack_from("<I", datos, 44)[0]
        primer_dir = struct.unpack_from("<I", datos, 48)[0]
        self._umbral_mini = struct.unpack_from("<I", datos, 56)[0]
        primer_minifat = struct.unpack_from("<I", datos, 60)[0]
        n_minifat = struct.unpack_from("<I", datos, 64)[0]
        primer_difat = struct.unpack_from("<I", datos, 68)[0]
        n_difat = struct.unpack_from("<I", datos, 72)[0]

        # DIFAT: los 109 primeros sectores de FAT van en la cabecera; el resto,
        # encadenados en sectores propios.
        difat = list(struct.unpack_from("<109I", datos, 76))
        sector = primer_difat
        por_sector = self._tam_sector // 4 - 1
        for _ in range(n_difat):
            if sector >= _CADENA_LIBRE:
                break
            base = self._desplazamiento(sector)
            difat += list(struct.unpack_from("<%dI" % por_sector, datos, base))
            sector = struct.unpack_from("<I", datos, base + self._tam_sector - 4)[0]

        self._fat = []
        for sector in (s for s in difat[:n_fat] if s < _CADENA_LIBRE):
            base = self._desplazamiento(sector)
            self._fat += list(
                struct.unpack_from("<%dI" % (self._tam_sector // 4), datos, base)
            )

        self._minifat = []
        sector = primer_minifat
        for _ in range(n_minifat):
            if sector >= _CADENA_LIBRE:
                break
            base = self._desplazamiento(sector)
            self._minifat += list(
                struct.unpack_from("<%dI" % (self._tam_sector // 4), datos, base)
            )
            sector = self._fat[sector]

        self._entradas = {}
        raiz = None
        crudo = self._cadena(primer_dir)
        for i in range(0, len(crudo) - 127, 128):
            e = crudo[i : i + 128]
            n_bytes = struct.unpack_from("<H", e, 64)[0]
            if n_bytes < 2:
                continue
            nombre = e[: n_bytes - 2].decode("utf-16-le", "replace")
            tipo = e[66]
            inicio = struct.unpack_from("<I", e, 116)[0]
            tam = struct.unpack_from("<Q", e, 120)[0]
            if tipo == 5:  # entrada raiz: su "stream" es el mini-stream
                raiz = (inicio, tam)
            else:
                self._entradas[nombre] = (inicio, tam)
        if raiz is None:
            raise DocIlegible("sin entrada raiz en el directorio OLE2")
        self._ministream = self._cadena(raiz[0])[: raiz[1]]

    def _desplazamiento(self, sector):
        return 512 + sector * self._tam_sector

    def _cadena(self, inicio):
        salida = bytearray()
        sector, pasos = inicio, 0
        while sector < _CADENA_LIBRE:
            base = self._desplazamiento(sector)
            salida += self._d[base : base + self._tam_sector]
            sector = self._fat[sector]
            pasos += 1
            if pasos > len(self._fat) + 2:
                raise DocIlegible("cadena de sectores ciclica")
        return bytes(salida)

    def stream(self, nombre):
        if nombre not in self._entradas:
            raise DocIlegible("falta el stream %r" % nombre)
        inicio, tam = self._entradas[nombre]
        if tam >= self._umbral_mini:
            return self._cadena(inicio)[:tam]
        salida = bytearray()
        sector = inicio
        while sector < _CADENA_LIBRE:
            base = sector * self._tam_mini
            salida += self._ministream[base : base + self._tam_mini]
            sector = self._minifat[sector]
        return bytes(salida[:tam])


def texto_de_doc(datos):
    """Devuelve el texto de un .doc de Word 97-2003, con las marcas de tabla.

    Las marcas se conservan a proposito: FIN_CELDA cierra celda, y duplicada
    cierra fila. Sin ellas no hay forma de recuperar la estructura de las tablas
    del layout, que es justo lo que hay que leer.
    """
    ole = _ContenedorOle2(datos)
    documento = ole.stream("WordDocument")
    if struct.unpack_from("<H", documento, 0)[0] != 0xA5EC:
        raise DocIlegible("el stream WordDocument no empieza por un FIB valido")

    # Bit 9 de las banderas del FIB dice cual de los dos streams de tabla manda.
    banderas = struct.unpack_from("<H", documento, 10)[0]
    tabla = ole.stream("1Table" if banderas & 0x0200 else "0Table")

    # El FIB lleva tres bloques de longitud variable antes del que interesa.
    p = 32
    p += 2 + struct.unpack_from("<H", documento, p)[0] * 2  # rgW97  (uint16)
    p += 2 + struct.unpack_from("<H", documento, p)[0] * 4  # rgLw97 (uint32)
    p += 2  # cbRgFcLcb
    # fcClx/lcbClx son la pareja 33 (contando desde 0) de rgFcLcb. En un FIB de
    # Word 97 eso cae en el desplazamiento absoluto 0x01A2, que sirve de control.
    if p + 33 * 8 != 0x01A2:
        raise DocIlegible("el FIB no tiene la forma esperada de Word 97-2003")
    fc_clx, lcb_clx = struct.unpack_from("<II", documento, p + 33 * 8)
    if lcb_clx == 0:
        raise DocIlegible("el FIB no declara piece table (lcbClx=0)")

    clx = tabla[fc_clx : fc_clx + lcb_clx]
    piezas = None
    i = 0
    while i < len(clx):
        marca = clx[i]
        if marca == 1:  # Prc de formato: se salta
            i += 3 + struct.unpack_from("<H", clx, i + 1)[0]
        elif marca == 2:  # Pcdt: aqui esta la piece table
            largo = struct.unpack_from("<I", clx, i + 1)[0]
            piezas = clx[i + 5 : i + 5 + largo]
            break
        else:
            raise DocIlegible("marca %d inesperada dentro del CLX" % marca)
    if piezas is None:
        raise DocIlegible("CLX sin piece table")

    n = (len(piezas) - 4) // 12
    cps = struct.unpack_from("<%dI" % (n + 1), piezas, 0)
    base_pcd = 4 * (n + 1)
    trozos = []
    for k in range(n):
        fc = struct.unpack_from("<I", piezas, base_pcd + k * 8 + 2)[0]
        comprimido = bool(fc & 0x40000000)
        desplazamiento = fc & 0x3FFFFFFF
        n_chars = cps[k + 1] - cps[k]
        if comprimido:  # 1 byte por caracter, cp1252
            ini = desplazamiento // 2
            trozos.append(documento[ini : ini + n_chars].decode("cp1252", "replace"))
        else:  # 2 bytes por caracter, UTF-16LE
            ini = desplazamiento
            trozos.append(
                documento[ini : ini + n_chars * 2].decode("utf-16-le", "replace")
            )
    return "".join(trozos)
