"""
Tests de la cadena de confianza. Todos menos uno corren SIN RED.

Lo que se prueba aqui no es que la descarga funcione -- eso se ve corriendo el
script. Se prueba lo contrario: que **cosas que no deberian pasar la
verificacion, no la pasan**. Un modulo de seguridad que solo se valida con el
caso bueno esta sin validar: acepta el caso bueno un `return True` puesto en la
primera linea.

    python -m pytest src/v2/test_cadena_confianza.py -v
    python -m pytest src/v2/test_cadena_confianza.py -v -m "not red"   (sin red)
"""

from __future__ import annotations

import datetime as dt
import ssl
from pathlib import Path

import pytest

from cadena_confianza import (
    HUELLA_SHA256,
    INTERMEDIA,
    CadenaInvalida,
    contexto_ssl,
    verificar_intermedia,
)


def _cert_falso(subject_igual_al_real: bool) -> bytes:
    """Un certificado autofirmado fabricado al vuelo, en PEM.

    Con `subject_igual_al_real=True` se hace pasar por la intermedia de la FNMT:
    mismo subject, mismo issuer declarado. Es el caso feo -- el atacante que sabe
    que nombre poner. Lo unico que no puede falsificar es la firma de la raiz.
    """
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    if subject_igual_al_real:
        nombre = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FNMT-RCM"),
                x509.NameAttribute(
                    NameOID.ORGANIZATIONAL_UNIT_NAME, "AC Componentes Informáticos"
                ),
            ]
        )
        emisor = x509.Name(
            [
                x509.NameAttribute(NameOID.COUNTRY_NAME, "ES"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FNMT-RCM"),
                x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "AC RAIZ FNMT-RCM"),
            ]
        )
    else:
        nombre = emisor = x509.Name(
            [x509.NameAttribute(NameOID.COMMON_NAME, "cualquier cosa")]
        )

    clave = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    ahora = dt.datetime.now(dt.timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(nombre)
        .issuer_name(emisor)
        .public_key(clave.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(ahora - dt.timedelta(days=1))
        .not_valid_after(ahora + dt.timedelta(days=365))
        .sign(clave, hashes.SHA256())
    )
    return cert.public_bytes(serialization.Encoding.PEM)


def test_la_intermedia_del_repo_verifica():
    """El caso bueno: el fichero versionado pasa los tres controles."""
    info = verificar_intermedia(INTERMEDIA.read_bytes())
    assert info["sha256"] == HUELLA_SHA256
    assert "AC RAIZ FNMT-RCM" in info["emisor"]


def test_se_rechaza_un_impostor_con_el_nombre_correcto():
    """El caso feo. Mismos nombres, firma que no es de la FNMT -> fuera.

    Si este test pasase a verde por accidente, la verificacion se habria
    degradado a comparar cadenas de texto, que es exactamente el fallo que se
    quiere evitar.
    """
    with pytest.raises(CadenaInvalida):
        verificar_intermedia(_cert_falso(subject_igual_al_real=True))


def test_se_rechaza_un_certificado_cualquiera():
    with pytest.raises(CadenaInvalida):
        verificar_intermedia(_cert_falso(subject_igual_al_real=False))


def test_se_rechaza_la_intermedia_real_con_un_bit_cambiado():
    """Un byte distinto en la clave publica invalida la firma de la raiz."""
    from cryptography import x509
    from cryptography.hazmat.primitives.serialization import Encoding

    real = x509.load_pem_x509_certificate(INTERMEDIA.read_bytes())
    der = bytearray(real.public_bytes(Encoding.DER))
    der[len(der) // 2] ^= 0xFF  # a mitad del cuerpo, no en la firma
    try:
        tocado = x509.load_der_x509_certificate(bytes(der))
    except ValueError:
        return  # ni siquiera parsea: rechazado antes todavia, tambien vale
    with pytest.raises(CadenaInvalida):
        verificar_intermedia(tocado.public_bytes(Encoding.PEM))


def test_el_contexto_nunca_sale_con_la_verificacion_floja():
    ctx = contexto_ssl()
    assert ctx.verify_mode == ssl.CERT_REQUIRED
    assert ctx.check_hostname is True


def test_el_modulo_no_contiene_ninguna_via_para_saltarse_la_verificacion():
    """Test de politica, no de comportamiento.

    Existe porque la tentacion es concreta y de una sola linea: el dia que la
    descarga falle con prisa, `CERT_NONE` esta a un teclazo. Que el repo se
    ponga en rojo al escribirlo es mas barato que descubrir tres meses despues
    que los datos oficiales se bajaron por un canal sin verificar.

    Se mira el AST y no el texto a proposito: la primera version de este test
    hacia `in` sobre el fuente y salto en rojo por las menciones de la propia
    docstring, donde `verify=False` aparece justo para decir que no se hace. Un
    `grep` no distingue mencionar de usar; el arbol sintactico si.
    """
    import ast

    fuente = (Path(__file__).parent / "cadena_confianza.py").read_text(encoding="utf-8")
    arbol = ast.parse(fuente)

    delitos = []
    for nodo in ast.walk(arbol):
        # ...CERT_NONE en cualquier posicion
        if isinstance(nodo, ast.Attribute) and nodo.attr == "CERT_NONE":
            delitos.append(f"linea {nodo.lineno}: uso de CERT_NONE")
        # verify=False / check_hostname=False como argumento de llamada
        if isinstance(nodo, ast.Call):
            for kw in nodo.keywords:
                if kw.arg in ("verify", "check_hostname") and isinstance(
                    kw.value, ast.Constant
                ):
                    if kw.value.value is False:
                        delitos.append(f"linea {nodo.lineno}: {kw.arg}=False")
        # ctx.check_hostname = False como asignacion
        if isinstance(nodo, ast.Assign) and isinstance(nodo.value, ast.Constant):
            if nodo.value.value is False:
                for destino in nodo.targets:
                    nombre = getattr(destino, "attr", getattr(destino, "id", ""))
                    if nombre == "check_hostname":
                        delitos.append(f"linea {nodo.lineno}: check_hostname = False")

    assert not delitos, "cadena_confianza.py se salta la verificacion:\n" + "\n".join(
        delitos
    )


@pytest.mark.red
def test_handshake_real_contra_infoelectoral():
    """El unico que necesita red. Prueba de punta a punta."""
    import socket

    from cadena_confianza import HOST

    ctx = contexto_ssl()
    with socket.create_connection((HOST, 443), timeout=30) as s:
        with ctx.wrap_socket(s, server_hostname=HOST) as ss:
            assert ss.version().startswith("TLS")
