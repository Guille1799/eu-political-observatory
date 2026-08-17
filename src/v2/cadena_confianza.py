"""
v2 -- Cadena de confianza para descargar de Infoelectoral SIN bajar la guardia.

El problema, y por que el diagnostico obvio era el equivocado
------------------------------------------------------------
Python no se conecta a `infoelectoral.interior.gob.es`: falla con
`CERTIFICATE_VERIFY_FAILED`. El navegador entra sin queja. La lectura facil de
ese sintoma es "la CA espanola (FNMT-RCM) no esta en el almacen de raices de
Mozilla, que es el que usa `certifi`". **Esa lectura es falsa y se comprobo:**

    $ grep -c FNMT $(python -c "import certifi;print(certifi.where())")
    -> certifi SI trae "AC RAIZ FNMT-RCM" y "AC RAIZ FNMT-RCM SERVIDORES SEGUROS"

Lo que pasa de verdad es otra cosa, y se ve pidiendo la cadena al servidor:

    $ openssl s_client -connect infoelectoral.interior.gob.es:443 -showcerts
     0 s:CN=*.interior.gob.es
       i:C=ES, O=FNMT-RCM, OU=AC Componentes Informaticos
    Verify return code: 21 (unable to verify the first certificate)

**El servidor manda solo el certificado de hoja y se deja fuera la intermedia**
`AC Componentes Informaticos`. Es un defecto de configuracion del servidor, no
un problema de raices: el ancla de confianza (`AC RAIZ FNMT-RCM`) ya esta
avalada, lo que falta es el eslabon de en medio que une una cosa con la otra.

Los navegadores lo disimulan porque, cuando la cadena viene incompleta, bajan
solos el eslabon que falta de la URL que el propio certificado declara en su
extension AIA (*Authority Information Access*). OpenSSL -- y por tanto Python,
`requests` y `curl` -- **no hacen eso**. De ahi que la fuente se abra en el
navegador y no desde codigo.

Por que esto NO se arregla desactivando la verificacion
------------------------------------------------------
Seria una linea (`verify=False`) y funcionaria. Y arruinaria el proyecto: la
mitad del valor de este trabajo es poder decir de donde sale cada numero. Un
dato oficial bajado por un canal que no se ha verificado no es un dato oficial,
es un dato parecido a uno oficial. Ademas aqui seria absurdo, porque **no hay
nada roto que justifique saltarse nada**: el certificado es autentico y su raiz
ya es de confianza.

Que hace este modulo
--------------------
Completa la cadena en vez de ignorarla:

1. Guarda la intermedia en el repo (`certs/`), versionada y auditable.
2. **Verifica su firma contra las raices que ya trae `certifi`** -- no se fia de
   ella por venir de una URL ni por coincidir con una huella escrita a mano.
   Es verificacion criptografica real (`verify_directly_issued_by`).
3. Comprueba de paso la huella SHA-256 fijada abajo y la validez temporal.
4. Devuelve un `SSLContext` con `certifi + intermedia` y la verificacion
   COMPLETA activa (`CERT_REQUIRED` + `check_hostname`).

**Confianza nueva anadida: ninguna.** La intermedia no se convierte en ancla:
se acepta solo porque una raiz ya avalada la firma. Si manana la FNMT rotase esa
intermedia, la verificacion fallaria de forma ruidosa -- que es lo que se quiere.

Refrescar el fichero del repo (solo si caduca o cambia):

    python src/v2/cadena_confianza.py --refrescar

Sin argumentos, hace un autodiagnostico y no escribe nada:

    python src/v2/cadena_confianza.py
"""

from __future__ import annotations

import hashlib
import ssl
import sys
import urllib.request
import warnings
from datetime import datetime, timezone
from pathlib import Path

# Raiz del repo: este fichero vive en <repo>/src/v2/
REPO = Path(__file__).resolve().parents[2]
CERTS = REPO / "certs"
INTERMEDIA = CERTS / "fnmt_ac_componentes_informaticos.pem"

# URL declarada por el propio certificado de hoja en su extension AIA
# ("CA Issuers"). Es HTTP a proposito y no pasa nada: lo que se descarga es un
# certificado, y su validez se comprueba por firma, no por el canal. Un
# intermediario que lo manipule produce un fichero que NO verifica contra la
# raiz, y este modulo lo rechaza.
AIA_URL = "http://www.cert.fnmt.es/certs/ACCOMP.crt"

# Huella del fichero versionado en `certs/`. Cruzada el 2026-08-17 contra la
# copia que el almacen de Windows tenia cacheada por una via independiente
# (SHA-1 C772B48D2385E502E84737DBE787B64311911247): identicas byte a byte.
HUELLA_SHA256 = "f038421f07f20d63a20d3691e5a178ab8459ebe570c1647b7690554ef23876ab"

HOST = "infoelectoral.interior.gob.es"
UA = "eu-political-observatory/v2 (descarga de fuente publica)"


class CadenaInvalida(RuntimeError):
    """La intermedia no supera la verificacion. Nunca se degrada a un aviso."""


def _raices_certifi() -> list:
    """Las raices de `certifi`, parseadas UNA A UNA y no de golpe.

    `x509.load_pem_x509_certificates` es todo-o-nada, y `certifi` incluye alguna
    raiz historica que `cryptography` ya solo acepta con un aviso de deprecacion
    (numero de serie no positivo, prohibido por RFC 5280) y que en una version
    futura rechazara. Cargando bloque a bloque, una raiz que no se pueda parsear
    se salta en vez de tumbar la verificacion entera -- y si la que se saltase
    fuese la que nos interesa, el resultado seria rechazar la intermedia, que es
    el lado seguro del fallo.
    """
    from cryptography import x509

    import certifi

    texto = Path(certifi.where()).read_text(encoding="utf-8")
    marca = "-----BEGIN CERTIFICATE-----"
    raices = []
    for bloque in texto.split(marca)[1:]:
        fin = bloque.find("-----END CERTIFICATE-----")
        if fin == -1:
            continue
        pem = (marca + bloque[: fin + len("-----END CERTIFICATE-----")]).encode()
        try:
            with warnings.catch_warnings():  # el aviso ya esta explicado arriba
                warnings.simplefilter("ignore")
                raices.append(x509.load_pem_x509_certificate(pem))
        except Exception:
            continue
    return raices


def verificar_intermedia(pem_bytes: bytes) -> dict:
    """Comprueba que estos bytes son la intermedia legitima. Lanza si no.

    Tres controles independientes; los tres tienen que pasar:
      - huella SHA-256 igual a la fijada arriba (integridad del fichero);
      - firma valida contra una raiz de `certifi` (esto es lo que de verdad
        establece la confianza: sin ello lo demas es solo un checksum);
      - dentro de su periodo de validez.
    """
    from cryptography import x509
    from cryptography.hazmat.primitives.serialization import Encoding

    cert = x509.load_pem_x509_certificate(pem_bytes)
    # La huella se calcula sobre el DER, que es la forma canonica del
    # certificado: dos ficheros PEM pueden diferir en saltos de linea y ser el
    # mismo certificado, asi que comparar el PEM crudo daria falsos negativos.
    huella = hashlib.sha256(cert.public_bytes(Encoding.DER)).hexdigest()
    if huella != HUELLA_SHA256:
        raise CadenaInvalida(
            f"huella SHA-256 inesperada:\n  esperada {HUELLA_SHA256}\n  obtenida {huella}"
        )

    emisor = None
    for raiz in _raices_certifi():
        if raiz.subject == cert.issuer:
            try:
                cert.verify_directly_issued_by(raiz)
            except Exception:
                continue
            emisor = raiz
            break
    if emisor is None:
        raise CadenaInvalida(
            "ninguna raiz de certifi firma esta intermedia -- no se usa. "
            f"Emisor declarado: {cert.issuer.rfc4514_string()}"
        )

    ahora = datetime.now(timezone.utc)
    if not (cert.not_valid_before_utc <= ahora <= cert.not_valid_after_utc):
        raise CadenaInvalida(
            f"intermedia fuera de validez ({cert.not_valid_before_utc:%Y-%m-%d} a "
            f"{cert.not_valid_after_utc:%Y-%m-%d})"
        )

    return {
        "subject": cert.subject.rfc4514_string(),
        "emisor": emisor.subject.rfc4514_string(),
        "caduca": cert.not_valid_after_utc.date().isoformat(),
        "sha256": huella,
    }


def contexto_ssl() -> ssl.SSLContext:
    """`SSLContext` con verificacion COMPLETA y la cadena ya completada.

    No existe ninguna variante de esta funcion que relaje la verificacion, y no
    debe anadirse: el dia que haga falta desactivarla, lo correcto es que la
    descarga falle y quede escrito por que.
    """
    import certifi

    if not INTERMEDIA.exists():
        raise CadenaInvalida(
            f"falta {INTERMEDIA.relative_to(REPO)} -- correr "
            "`python src/v2/cadena_confianza.py --refrescar`"
        )
    pem = INTERMEDIA.read_bytes()
    verificar_intermedia(pem)  # lanza si algo no cuadra

    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.load_verify_locations(cadata=pem.decode("ascii"))
    ctx.verify_mode = ssl.CERT_REQUIRED
    ctx.check_hostname = True
    return ctx


def refrescar() -> dict:
    """Vuelve a bajar la intermedia del AIA y la guarda SOLO si verifica."""
    from cryptography import x509
    from cryptography.hazmat.primitives.serialization import Encoding

    req = urllib.request.Request(AIA_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        crudo = resp.read()
    # La FNMT lo sirve en DER; se acepta PEM por si eso cambia.
    try:
        cert = x509.load_der_x509_certificate(crudo)
    except ValueError:
        cert = x509.load_pem_x509_certificate(crudo)
    pem = cert.public_bytes(Encoding.PEM)
    info = verificar_intermedia(pem)  # lanza antes de escribir nada
    CERTS.mkdir(parents=True, exist_ok=True)
    INTERMEDIA.write_bytes(pem)
    return info


def _diagnostico() -> int:
    import socket

    print(f"repo:        {REPO}")
    print(f"intermedia:  {INTERMEDIA.relative_to(REPO)}")
    if not INTERMEDIA.exists():
        print("  AUSENTE -- correr con --refrescar")
        return 1
    try:
        info = verificar_intermedia(INTERMEDIA.read_bytes())
    except CadenaInvalida as exc:
        print(f"  RECHAZADA: {exc}")
        return 1
    for k, v in info.items():
        print(f"  {k:8s} {v}")

    print(f"\nhandshake con {HOST}:")
    try:
        ctx = contexto_ssl()
        with socket.create_connection((HOST, 443), timeout=30) as s:
            with ctx.wrap_socket(s, server_hostname=HOST) as ss:
                print(f"  VERIFICADO -- {ss.version()} / {ss.cipher()[0]}")
    except Exception as exc:
        print(f"  FALLO: {type(exc).__name__}: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    if "--refrescar" in sys.argv[1:]:
        try:
            datos = refrescar()
        except CadenaInvalida as e:
            print(f"NO se escribio nada -- {e}")
            raise SystemExit(1)
        print(f"intermedia actualizada y verificada: {datos}")
        raise SystemExit(0)
    raise SystemExit(_diagnostico())
