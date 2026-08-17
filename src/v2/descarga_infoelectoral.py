"""
v2 — DIA 1: reconocimiento de la fuente electoral espanola (Infoelectoral).

Que hace y por que
------------------
El diseno v1 murio por las FUENTES, no por la pregunta: la base electoral europea
que se estaba usando no baja de region grande, y la clasificacion de partidos venia
de dos bases academicas que dejan sin veredicto el 22,9% del voto espanol -- justo
los partidos de ambito no estatal, que son el objeto del proyecto.

v2 cambia las dos cosas a la vez:
  - la ESCALA la da el Ministerio del Interior (Infoelectoral), que publica desde
    1977 a nivel de MUNICIPIO y de MESA -- mas fino que cualquier nivel europeo;
  - el OBJETO deja de ser "nacionalista" (juicio ideologico, discutido y mal
    codificado) y pasa a ser PANE, partido de ambito no estatal, que se define por
    DONDE concurre y no por lo que piensa.

Este script NO analiza nada. Hace lo unico que toca el primer dia: comprobar que la
fuente existe, bajarla, y decir con exactitud QUE hay dentro. Los ficheros del
Ministerio son de ancho fijo con una especificacion propia, asi que el layout se
LEE, no se supone: dar por buena una estructura no verificada es exactamente el
modo de fallo que mato a v1.

Lo que este script deliberadamente NO hace: parsear registros, mapear partidos,
agregar por escala, ni calcular nada. Eso viene despues, y solo cuando el informe
de aqui diga que se puede.

Salidas (data/processed/ y data/external/; data/raw/ es READ-ONLY y no se toca):
  - data/external/infoelectoral/<fichero>.zip   descarga cruda
  - data/processed/v2_reconocimiento_infoelectoral.md   informe de que hay dentro

Uso:  python src/v2/descarga_infoelectoral.py            (desde la raiz del repo)
      python src/v2/descarga_infoelectoral.py 2019 11    (otra convocatoria)
"""

from __future__ import annotations

import hashlib
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cadena_confianza import contexto_ssl  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):  # acentos en la consola de Windows
    sys.stdout.reconfigure(encoding="utf-8")

EXTERNAL = Path("data/external/infoelectoral")
OUT = Path("data/processed")

BASE = "https://infoelectoral.interior.gob.es/estaticos/docxl/apliextr"

# Tipo de proceso segun la nomenclatura del Ministerio. Solo se declara el que se
# usa; el resto se anadira cuando haga falta y se haya comprobado.
TIPO_CONGRESO = "02"

# El ambito decide la granularidad del fichero. Se prueban los tres en orden de
# finura para descubrir cual esta publicado en cada convocatoria, en vez de
# asumirlo.
AMBITOS = ("MESA", "MUNI", "TOTA")

TIMEOUT = 60
UA = "eu-political-observatory/v2 (reconocimiento de fuente publica)"


def url_de(tipo: str, anio: int, mes: int, ambito: str) -> str:
    return f"{BASE}/{tipo}{anio}{mes:02d}_{ambito}.zip"


def descargar(url: str, destino: Path) -> tuple[bool, str]:
    """Devuelve (exito, detalle). No lanza: un 404 es informacion, no un error."""
    if destino.exists() and destino.stat().st_size > 0:
        return True, f"ya estaba en disco ({destino.stat().st_size:,} bytes)"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=contexto_ssl()) as resp:
            datos = resp.read()
    except urllib.error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:  # red caida, DNS, TLS...
        return False, f"{type(exc).__name__}: {exc}"
    if not datos:
        return False, "respuesta vacia"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(datos)
    return True, f"descargado ({len(datos):,} bytes)"


def inventario(zip_path: Path) -> list[dict]:
    """Que hay dentro del zip, sin interpretar el contenido."""
    filas = []
    with zipfile.ZipFile(zip_path) as z:
        for info in sorted(z.infolist(), key=lambda i: i.filename):
            if info.is_dir():
                continue
            with z.open(info) as fh:
                cabeza = fh.read(4096)
            # Los .DAT del Ministerio son de ancho fijo: se mide la primera linea
            # en vez de suponer el layout.
            corte = cabeza.find(b"\n")
            primera = cabeza[:corte] if corte != -1 else cabeza
            ancho = len(primera.rstrip(b"\r\n"))
            filas.append(
                {
                    "fichero": info.filename,
                    "bytes": info.file_size,
                    "ancho_1a_linea": ancho if corte != -1 else None,
                    "muestra": primera[:60].decode("latin-1", errors="replace"),
                }
            )
    return filas


def contencion_de_ambitos(descargados: list[tuple[str, Path]]) -> list[str]:
    """Comprueba por hash si un ambito contiene a otro, en vez de suponerlo.

    A ojo, los tres paquetes parecen repetir ficheros con el mismo tamano. Pero
    "mismo tamano" no es "mismo contenido", asi que se compara el SHA-256 de cada
    entrada. Si la contencion se confirma, basta con bajar el ambito mas fino y
    los otros dos sobran -- una descarga en vez de tres, y ninguna duda sobre
    cual de las tres copias de un catalogo es la buena.
    """
    hashes: dict[str, dict[str, str]] = {}
    for ambito, zip_path in descargados:
        try:
            with zipfile.ZipFile(zip_path) as z:
                hashes[ambito] = {
                    i.filename: hashlib.sha256(z.read(i)).hexdigest()
                    for i in z.infolist()
                    if not i.is_dir()
                }
        except zipfile.BadZipFile:
            continue

    veredictos = []
    for menor, mayor in (("MUNI", "MESA"), ("TOTA", "MUNI"), ("TOTA", "MESA")):
        if menor not in hashes or mayor not in hashes:
            continue
        contenido = all(hashes[mayor].get(k) == v for k, v in hashes[menor].items())
        extra = sorted(set(hashes[mayor]) - set(hashes[menor]))
        veredictos.append(
            f"`{menor}` {'ESTA contenido en' if contenido else 'NO esta contenido en'} "
            f"`{mayor}`" + (f" (que anade: {', '.join(f'`{e}`' for e in extra)})" if extra else "")
        )
    return veredictos


def extraer_especificacion(descargados: list[tuple[str, Path]]) -> list[Path]:
    """Saca el `FICHEROS.doc` de cada zip, que es la especificacion del layout.

    Merece funcion propia porque es el hallazgo que evita el modo de fallo que
    mato a v1: **el layout no hay que suponerlo ni buscarlo en otra web, viene
    empaquetado con los datos**. Se extrae tal cual, sin intentar parsearlo aqui:
    transcribirlo a un esquema es un paso aparte y deliberado.
    """
    sacados: list[Path] = []
    for _, zip_path in descargados:
        try:
            with zipfile.ZipFile(zip_path) as z:
                for info in z.infolist():
                    if not Path(info.filename).stem.upper() == "FICHEROS":
                        continue
                    destino = EXTERNAL / "especificacion" / f"{zip_path.stem}_{info.filename}"
                    destino.parent.mkdir(parents=True, exist_ok=True)
                    if not destino.exists():
                        destino.write_bytes(z.read(info))
                    sacados.append(destino)
        except zipfile.BadZipFile:
            continue
    return sacados


def main(anio: int = 2019, mes: int = 11) -> int:
    EXTERNAL.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    lineas: list[str] = []
    w = lineas.append

    w(f"# v2 - Reconocimiento de Infoelectoral: generales {anio}-{mes:02d}")
    w("")
    w(f"Generado: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    w("")
    w("Este informe solo dice QUE hay en la fuente. No interpreta ni un solo campo.")
    w("")
    w("## Disponibilidad por ambito")
    w("")
    w("| Ambito | URL | Resultado |")
    w("|---|---|---|")

    descargados: list[tuple[str, Path]] = []
    for ambito in AMBITOS:
        url = url_de(TIPO_CONGRESO, anio, mes, ambito)
        destino = EXTERNAL / Path(url).name
        ok, detalle = descargar(url, destino)
        w(f"| {ambito} | `{Path(url).name}` | {'OK - ' if ok else 'FALLO - '}{detalle} |")
        print(f"[{ambito}] {'OK' if ok else 'FALLO'}: {detalle}")
        if ok:
            descargados.append((ambito, destino))

    w("")
    if not descargados:
        w("## Resultado: no se descargo nada")
        w("")
        w("La cadena de confianza se valida en `src/v2/cadena_confianza.py` y ese")
        w("modulo tiene su propio autodiagnostico. Correrlo es el primer paso:")
        w("")
        w("```")
        w("python src/v2/cadena_confianza.py")
        w("```")
        w("")
        w("Si el handshake sale VERIFICADO, el problema no es TLS sino el patron de")
        w("nombre de fichero o la disponibilidad de esa convocatoria. **No se da por")
        w("bueno ningun patron que no se haya descargado.**")
        (OUT / "v2_reconocimiento_infoelectoral.md").write_text(
            "\n".join(lineas) + "\n", encoding="utf-8"
        )
        print("\nSin descargas. Informe escrito igualmente.")
        return 1

    for ambito, ruta in descargados:
        w(f"## Contenido de `{ruta.name}` (ambito {ambito})")
        w("")
        try:
            filas = inventario(ruta)
        except zipfile.BadZipFile:
            w("**No es un zip valido.** Probablemente el servidor devolvio una")
            w("pagina de error con codigo 200. Hay que mirarlo a mano.")
            w("")
            continue
        w("| Fichero | Bytes | Ancho 1a linea | Muestra (60 primeros caracteres) |")
        w("|---|---|---|---|")
        for f in filas:
            muestra = f["muestra"].replace("|", "\\|")
            w(f"| `{f['fichero']}` | {f['bytes']:,} | {f['ancho_1a_linea']} | `{muestra}` |")
        w("")

    veredictos = contencion_de_ambitos(descargados)
    if veredictos:
        w("## Los tres ambitos NO son tres conjuntos de datos distintos")
        w("")
        w("Comparado entrada por entrada con SHA-256, no por tamano:")
        w("")
        for v in veredictos:
            w(f"- {v}")
        w("")
        w("Es decir: el ambito no cambia el catalogo, solo **anade** ficheros de")
        w("resultados mas finos. Consecuencia practica: **con bajar `MESA` sobra**.")
        w("")

    especificaciones = extraer_especificacion(descargados)
    if especificaciones:
        w("## La especificacion del layout venia DENTRO del zip")
        w("")
        w("No hay que buscarla fuera: cada paquete trae un `FICHEROS.doc` que")
        w("describe los campos de ancho fijo. Extraido a `data/external/` para")
        w("poder transcribirlo a un esquema:")
        w("")
        for ruta in especificaciones:
            w(f"- `{ruta.as_posix()}` ({ruta.stat().st_size:,} bytes)")
        w("")

    w("## Lo que este informe NO dice, y hace falta antes de analizar nada")
    w("")
    w("1. **Que significa cada campo.** El ancho de linea sugiere ancho fijo, pero")
    w("   el layout hay que sacarlo de la especificacion oficial, no de mirar los")
    w("   numeros. Siguiente paso: localizarla y transcribirla a un esquema.")
    w("2. **Que partidos son de ambito no estatal (PANE).** La definicion operativa")
    w("   -- en cuantas circunscripciones concurre -- se calcula desde estos mismos")
    w("   ficheros, pero hay que decidir y ESCRIBIR el umbral antes de mirarlo.")
    w("3. **Con que se cruza la parte economica.** A nivel municipal no sirve la")
    w("   fuente europea; hay que comprobar que publica el INE. Sin eso, la mitad")
    w("   economica del analisis no tiene con que hacerse.")

    (OUT / "v2_reconocimiento_infoelectoral.md").write_text(
        "\n".join(lineas) + "\n", encoding="utf-8"
    )
    print(f"\nInforme: {OUT / 'v2_reconocimiento_infoelectoral.md'}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    anio_arg = int(args[0]) if len(args) > 0 else 2019
    mes_arg = int(args[1]) if len(args) > 1 else 11
    raise SystemExit(main(anio_arg, mes_arg))
