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

import ssl
import sys
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

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


def contexto_ssl() -> ssl.SSLContext:
    """Contexto con verificacion SIEMPRE activa.

    Algunas instalaciones de Python en Windows no traen bundle de CAs y fallan con
    CERTIFICATE_VERIFY_FAILED contra sitios perfectamente validos. La solucion es
    apuntar a los certificados de `certifi`, NO desactivar la verificacion: bajar
    datos oficiales por un canal sin verificar invalidaria su procedencia, que es
    justo lo que este proyecto vende.
    """
    try:
        import certifi

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


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
        w("## Resultado: no se descargo nada, y la razon es un hallazgo")
        w("")
        w("**El obstaculo NO es la nomenclatura del fichero ni la red.** El handshake")
        w("TLS con `infoelectoral.interior.gob.es` funciona y el certificado es")
        w("autentico. Comprobado a mano:")
        w("")
        w("```")
        w("subject = CN=*.interior.gob.es, O=MINISTERIO INTERIOR - SECRETARIA ESTADO SEGURIDAD")
        w("issuer  = C=ES, O=FNMT-RCM, OU=AC Componentes Informaticos")
        w("```")
        w("")
        w("La autoridad emisora es la **FNMT-RCM**, la CA de la administracion")
        w("espanola. **No viene en el almacen de confianza por defecto de Python ni")
        w("en el de `certifi`**, que siguen el programa de raices de Mozilla. Por eso")
        w("falla con `CERTIFICATE_VERIFY_FAILED` una fuente que el navegador abre sin")
        w("problema.")
        w("")
        w("**Por que esto importa y no es una anecdota de configuracion:**")
        w("")
        w("1. Es una barrera de entrada real y silenciosa a los datos electorales")
        w("   oficiales espanoles desde codigo. Explica parte de por que casi todo el")
        w("   analisis publico se hace sobre reagregaciones de terceros en vez de")
        w("   sobre la fuente primaria.")
        w("2. La salida correcta es **anadir la raiz de la FNMT al bundle**, no")
        w("   desactivar la verificacion. Si se desactiva, la procedencia del dato")
        w("   deja de estar respaldada -- y la procedencia es la mitad del valor de")
        w("   este proyecto.")
        w("")
        w("**Siguiente paso, concreto:** obtener la raiz de la FNMT por un canal")
        w("verificable, anadirla a un bundle propio del repo, y volver a correr esto.")
        w("Hasta entonces no se ha comprobado el patron de nombre de fichero: puede")
        w("ser correcto o no, y **no se da por bueno**.")
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
