"""Configuracion de pytest para los modulos de v2.

Los scripts de v2 se ejecutan sueltos (`python src/v2/loquesea.py`) y por eso se
importan entre si por nombre plano. Esto hace que pytest los encuentre igual, sin
convertir el directorio en un paquete y sin tocar como se lanzan a mano.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "red: necesita conexion a internet (desactivar con -m 'not red')"
    )
