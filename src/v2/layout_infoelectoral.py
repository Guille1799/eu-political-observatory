"""
v2 -- El layout de los ficheros de Infoelectoral, leido de su propia especificacion.

Que hace
--------
Los ficheros del Ministerio del Interior son de ancho fijo. Su especificacion no
esta en una web que haya que buscar ni en un paquete de terceros: viaja DENTRO del
zip de descarga, en `FICHEROS.doc`. Este modulo la abre, la parsea y devuelve un
esquema con los 12 tipos de fichero y sus campos.

La regla es "se lee, no se supone", y aqui es literal: nada del layout esta escrito
a mano en este fichero. Si el Ministerio cambia la especificacion en una
convocatoria futura, el esquema cambia solo y los tests lo cazan.

Lo que se comprobo al escribirlo, y no estaba en la especificacion
-----------------------------------------------------------------
La especificacion dice, en su primer parrafo, que los registros van "con
delimitador de registro CR+LF". Es FALSO en los ficheros publicados de 2019-11
(y en 2015-12, 2016-06 y 2019-04): el delimitador es LF a secas, sin CR. Pero
NO es falso siempre -- 2023-07 SI trae CR+LF, y solo en su fichero 04
(candidaturas): sus 5.099 registros terminan todos en `\\r\\n`, mientras que
los otros nueve ficheros de ese mismo zip siguen en LF a secas. El delimitador
no es una propiedad de la convocatoria, es una propiedad de cada fichero.

No es una pega academica. Un lector que confie en esa frase y descuente dos bytes
por registro se desplaza un byte por linea, y a partir del segundo registro lee
todos los campos corridos -- con numeros que siguen pareciendo numeros. Y un
lector que en su lugar asuma "siempre LF" porque asi salio en cuatro
convocatorias comete el mismo error con el signo cambiado el dia que lee el 04
de 2023-07: cada registro le sobra un byte. Es el modo de fallo silencioso que
el proyecto quiere evitar, y sale de la unica forma en que podia salir:
contrastando la especificacion Y el propio fichero contra el fichero real, en
las cinco convocatorias, no en una.

Por eso `longitud_registro` es la longitud del REGISTRO (sin delimitador), y
quien lea los ficheros parte por lineas con `lineas_de_registro` -- que acepta
LF o CR+LF -- en vez de trocear por posiciones absolutas o por `\\n` a pelo.

Uso
---
    from layout_infoelectoral import esquema_de_zip
    esquema = esquema_de_zip("data/external/infoelectoral/02201911_MESA.zip")
    esquema["10"].longitud_registro        # 36
    esquema["10"].campo("Votos").rebanada   # slice(29, 36)

O como script, para ver el esquema por pantalla:

    python src/v2/layout_infoelectoral.py data/external/infoelectoral/02201911_MESA.zip
"""

from __future__ import annotations

import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

from lector_doc import texto_de_doc

NOMBRE_ESPECIFICACION = "FICHEROS.doc"

# Cabecera de tabla de layout, tal cual aparece en el .doc.
_CABECERA_CAMPOS = ("Inicio", "Fin", "Tipo", "Long.", "Descripcion")

# "03xxaamm.DAT", y tambien "1104aamm.DAT" (ficheros 11 y 12, solo municipales).
_PATRON_FICHERO = re.compile(r"^(\d{2})(?:xx|\d{2})aamm\.DAT$", re.IGNORECASE)
_PATRON_TITULO = re.compile(r"^(\d{1,2})\.-\s+(.*)$", re.DOTALL)

TIPOS_VALIDOS = ("Num.", "Alf.")


class EspecificacionIlegible(Exception):
    """La especificacion no tiene la forma esperada. Nunca se adivina el layout."""


@dataclass(frozen=True)
class Campo:
    """Un campo de ancho fijo. `inicio` y `fin` son 1-based e inclusivos."""

    inicio: int
    fin: int
    tipo: str
    longitud: int
    descripcion: str

    @property
    def rebanada(self):
        """Rebanada 0-based para trocear un registro ya sin delimitador."""
        return slice(self.inicio - 1, self.fin)

    @property
    def es_numerico(self):
        return self.tipo == "Num."


@dataclass(frozen=True)
class EsquemaFichero:
    codigo: str  # "01" .. "12"
    patron: str  # "03xxaamm.DAT"
    titulo: str
    campos: tuple

    @property
    def longitud_registro(self):
        """Bytes de un registro, SIN el delimitador de linea."""
        return self.campos[-1].fin

    def campo(self, fragmento):
        """El campo cuya descripcion contiene `fragmento` (sin distinguir mayusculas).

        Revienta si no coincide ninguno, y tambien si coinciden varios: una
        aguja ambigua resuelta en silencio con "el primero que aparezca" es el
        mismo riesgo que un hueco entre campos (`_validar_campos`) -- una
        lectura plausible y equivocada. El caso ambiguo es real, no
        hipotetico: en el fichero 03, "Codigo de la candidatura" coincide con
        la candidatura Y con sus tres cabeceras de acumulacion.
        """
        aguja = fragmento.lower()
        coincidencias = [c for c in self.campos if aguja in c.descripcion.lower()]
        if not coincidencias:
            raise KeyError("ningun campo de %s menciona %r" % (self.patron, fragmento))
        if len(coincidencias) > 1:
            raise EspecificacionIlegible(
                "%s: %r es ambiguo, coincide con %d campos (%s)"
                % (
                    self.patron,
                    fragmento,
                    len(coincidencias),
                    ", ".join("%d-%d" % (c.inicio, c.fin) for c in coincidencias),
                )
            )
        return coincidencias[0]

    def nombre_fichero(self, tipo_eleccion, anio, mes):
        """Nombre real del .dat: p.ej. ("02", 2019, 11) -> "03021911.DAT"."""
        return "%s%02d%02d%02d.DAT" % (
            self.codigo,
            int(tipo_eleccion),
            int(anio) % 100,
            int(mes),
        )


def _sin_tildes(texto):
    return (
        texto.replace("á", "a")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ñ", "n")
        .replace("Á", "A")
        .replace("É", "E")
        .replace("Í", "I")
        .replace("Ó", "O")
        .replace("Ú", "U")
        .replace("Ñ", "N")
    )


def _normalizar(celda):
    """Aplana los saltos de linea internos de una celda a espacios simples."""
    return " ".join(celda.replace("\x0c", " ").split())


def _filas(texto):
    """Trocea el texto en filas de tabla; cada fila es una lista de celdas."""
    return [f.split("\x07") for f in texto.split("\x07\x07")]


def _es_cabecera_de_campos(fila):
    if len(fila) < 5:
        return False
    return [_sin_tildes(_normalizar(c)) for c in fila[:5]] == list(_CABECERA_CAMPOS)


def parsear_especificacion(texto):
    """Devuelve {codigo: EsquemaFichero} a partir del texto del FICHEROS.doc."""
    filas = _filas(texto)
    esquemas = {}

    for i, fila in enumerate(filas):
        # El patron del nombre de fichero es la ultima linea de una celda suelta:
        # en el primer fichero comparte celda con todo el preambulo del documento.
        lineas = [l for l in _normalizar(fila[0]).split(" ") if l]
        if not lineas:
            continue
        m = _PATRON_FICHERO.match(lineas[-1])
        if not m:
            continue
        codigo, patron = m.group(1), lineas[-1]

        titulo_m = _PATRON_TITULO.match(_normalizar(filas[i + 1][0]))
        if not titulo_m or titulo_m.group(1).zfill(2) != codigo:
            raise EspecificacionIlegible(
                "el patron %s no va seguido de su titulo numerado" % patron
            )

        # Entre el titulo y las filas de campos hay una cabecera de dos niveles
        # ("Posiciones"/"Datos" y luego Inicio/Fin/Tipo/Long./Descripcion).
        j = i + 2
        while j < len(filas) and not _es_cabecera_de_campos(filas[j]):
            if j > i + 4:
                raise EspecificacionIlegible(
                    "no aparece la cabecera de campos tras %s" % patron
                )
            j += 1

        campos = []
        for fila_campo in filas[j + 1 :]:
            celdas = [_normalizar(c) for c in fila_campo[:5]]
            if len(celdas) < 5 or not celdas[0].isdigit():
                break  # se acabo la tabla (OBSERVACIONES, o el fichero siguiente)
            inicio, fin, tipo, longitud, descripcion = celdas
            if tipo not in TIPOS_VALIDOS:
                raise EspecificacionIlegible(
                    "tipo %r desconocido en %s, posicion %s" % (tipo, patron, inicio)
                )
            campos.append(
                Campo(int(inicio), int(fin), tipo, int(longitud), descripcion)
            )

        if not campos:
            raise EspecificacionIlegible("%s no declara ningun campo" % patron)
        _validar_campos(patron, campos)
        esquemas[codigo] = EsquemaFichero(codigo, patron, titulo_m.group(2), tuple(campos))

    if not esquemas:
        raise EspecificacionIlegible("no se reconocio ninguna tabla de layout")
    return esquemas


def _validar_campos(patron, campos):
    """Un layout de ancho fijo solo vale si tapa el registro entero, sin huecos.

    Se comprueba aqui y no solo en los tests: un esquema con un hueco de un byte
    produce lecturas plausibles y equivocadas, asi que revienta al construirse.
    """
    esperado = 1
    for c in campos:
        if c.fin - c.inicio + 1 != c.longitud:
            raise EspecificacionIlegible(
                "%s: el campo %d-%d dice longitud %d" % (patron, c.inicio, c.fin, c.longitud)
            )
        if c.inicio != esperado:
            raise EspecificacionIlegible(
                "%s: se esperaba que el siguiente campo empezase en %d y empieza en %d"
                % (patron, esperado, c.inicio)
            )
        esperado = c.fin + 1


def lineas_de_registro(datos):
    """Trocea `datos` en registros SIN delimitador, sea el delimitador LF o CR+LF.

    La especificacion promete CR+LF; en la practica varia por FICHERO, no solo
    por convocatoria (ver docstring del modulo). Partir siempre por `\\n` a
    secas deja un `\\r` colgando al final de cada registro cuando el fichero
    si trae CR+LF, y ese byte de mas se cuela en cualquier comparacion de
    longitud. Aqui se quita si esta, y no se asume que tenga que estar.
    """
    return [linea[:-1] if linea.endswith(b"\r") else linea for linea in datos.split(b"\n")]


def esquema_de_zip(ruta_zip):
    """Lee la especificacion incrustada en el zip de descarga y la parsea."""
    with zipfile.ZipFile(ruta_zip) as z:
        nombres = [n for n in z.namelist() if n.upper().endswith("FICHEROS.DOC")]
        if not nombres:
            raise EspecificacionIlegible(
                "%s no lleva dentro la especificacion (%s)"
                % (ruta_zip, NOMBRE_ESPECIFICACION)
            )
        crudo = z.read(nombres[0])
    return parsear_especificacion(texto_de_doc(crudo))


def esquema_de_doc(ruta_doc):
    """Lee la especificacion desde un .doc ya extraido."""
    return parsear_especificacion(texto_de_doc(Path(ruta_doc).read_bytes()))


def _imprimir(esquemas):
    for codigo in sorted(esquemas):
        e = esquemas[codigo]
        print("\n%s  %s" % (e.patron, e.titulo))
        print("  registro de %d bytes, %d campos" % (e.longitud_registro, len(e.campos)))
        for c in e.campos:
            print(
                "    %4d-%-4d %-5s %3d  %s"
                % (c.inicio, c.fin, c.tipo, c.longitud, c.descripcion[:70])
            )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__.strip().splitlines()[-1])
        raise SystemExit(2)
    ruta = Path(sys.argv[1])
    _imprimir(esquema_de_zip(ruta) if ruta.suffix.lower() == ".zip" else esquema_de_doc(ruta))
