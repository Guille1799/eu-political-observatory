"""Reproduce y cierra BUG-COBERTURA-PARTIDOS-PY-REDECLARA.

`cobertura_partidos.py` redeclaraba `NATIVISM_THRESHOLD = 7.0` en vez de importarlo de
`parameters.py`, que es la fuente unica que su propio docstring dice ser ("Un corte
metodologico vive en UN solo sitio... los scripts lo importan, no lo redeclaran"). Si
alguien cambia el umbral en parameters.py, cobertura_partidos.py debe heredarlo, no
seguir imprimiendo un informe con su propia copia.

No usa data/raw/ (no existe en este worktree): solo inspecciona el modulo importado y
su codigo fuente.
"""
import ast
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from parameters import NATIVISM_THRESHOLD
import cobertura_partidos


def test_el_umbral_se_lee_de_parameters():
    # El valor en tiempo de ejecucion de cobertura_partidos tiene que ser EL MISMO
    # objeto/valor que declara parameters.py, no una copia que coincide por casualidad.
    assert cobertura_partidos.NATIVISM_THRESHOLD == NATIVISM_THRESHOLD, (
        "cobertura_partidos.NATIVISM_THRESHOLD no coincide con parameters.NATIVISM_"
        "THRESHOLD"
    )

    # Y no puede ser una redeclaracion local: el fichero no puede volver a asignarle
    # un literal a NATIVISM_THRESHOLD. Se comprueba con AST (no con grep de texto) para
    # no depender de como se formatee la linea, y para no confundir una asignacion con
    # el `import` que la reemplaza (un ImportFrom no es un ast.Assign).
    codigo_fuente = Path(cobertura_partidos.__file__).read_text(encoding="utf-8")
    arbol = ast.parse(codigo_fuente)
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Assign):
            for objetivo in nodo.targets:
                if isinstance(objetivo, ast.Name) and objetivo.id == "NATIVISM_THRESHOLD":
                    raise AssertionError(
                        "cobertura_partidos.py sigue asignando NATIVISM_THRESHOLD "
                        "localmente en vez de importarlo de parameters.py"
                    )


if __name__ == "__main__":
    test_el_umbral_se_lee_de_parameters()
    print("1 correcto, 0 fallos")
