"""Reproduce y cierra BUG-LA-COLUMNA-PUBLICADA-MEJOR.

`mejor_cuota_nacional_%` (cobertura_partidos.py) sumaba `validvote` sobre las filas del
PROPIO partido en vez de sobre la tabla region-eleccion deduplicada. `validvote` esta
repetido en cada fila de partido, asi que un partido que solo presenta candidatura en
una region (como el Ulster Unionist Party, que solo concurre en Irlanda del Norte) salia
con una "cuota nacional" calculada sobre el validvote de esa unica region, no del pais
entero -- publicado como 34,52 % cuando la cuota real de 1992 fue 0,81 %.

No usa data/raw/ (no existe en este worktree): construye un `par` sintetico con la
misma forma que produce `marcar_cobertura()` sobre EU-NED.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cobertura_partidos import cuota_nacional_por_partido


def test_cuota_nacional_usa_el_validvote_del_pais():
    # Pais GB, eleccion 1992, dos regiones. El partido X (como UUP) solo presenta
    # candidatura en la region A; el partido Y cubre la region B. `validvote` esta
    # repetido en cada fila de partido, igual que en EU-NED real.
    par = pd.DataFrame([
        # country_code, region_id, year, pf, nombre, residual, partyvote, validvote
        ("GB", "A", 1992, 1, "X", False, 100, 1000),
        ("GB", "B", 1992, 2, "Y", False, 900, 9000),
    ], columns=["country_code", "region_id", "year", "pf", "nombre", "residual",
                "partyvote", "validvote"])

    mejor = cuota_nacional_por_partido(par)

    # El validvote nacional real es 1000 + 9000 = 10000 (deduplicado por region), no los
    # 1000 de la unica region donde X tiene fila. Cuota correcta de X: 100*100/10000=1.0%.
    cuota_x = mejor.loc[("GB", "X")]
    assert abs(cuota_x - 1.0) < 1e-9, (
        f"mejor_cuota_nacional_%% de X deberia ser 1.0 (100 votos sobre 10000 "
        f"validvote nacional), salio {cuota_x}: sigue sumando validvote solo sobre "
        f"las filas del propio partido"
    )


if __name__ == "__main__":
    test_cuota_nacional_usa_el_validvote_del_pais()
    print("1 correcto, 0 fallos")
