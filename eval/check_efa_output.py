"""
check_efa_output.py — Verifica integridad del pipeline EFA para España.

Exit 0: todo OK (imprime resumen)
Exit 1: algún check falló (imprime qué falló)
"""

import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas no disponible — instalar en el entorno R/Python del proyecto")
    sys.exit(1)

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPAIN_DIR = os.path.join(PROJECT_DIR, "data", "processed", "ess", "spain")

LOADINGS_FILE = os.path.join(SPAIN_DIR, "spain_efa_loadings.csv")
COMMUNALITIES_FILE = os.path.join(SPAIN_DIR, "spain_efa_communalities.csv")
SUMMARY_FILE = os.path.join(SPAIN_DIR, "spain_efa_summary.txt")

FAILED = []


def fail(msg: str):
    FAILED.append(msg)
    print(f"❌ {msg}")


# Check 1: Archivos existen
for fpath, name in [(LOADINGS_FILE, "spain_efa_loadings.csv"),
                    (COMMUNALITIES_FILE, "spain_efa_communalities.csv"),
                    (SUMMARY_FILE, "spain_efa_summary.txt")]:
    if not os.path.exists(fpath):
        fail(f"Archivo no encontrado: {name}")

if FAILED:
    sys.exit(1)

# Check 2: Dimensiones de loadings (25-45 vars, 5-15 factores)
try:
    loadings = pd.read_csv(LOADINGS_FILE, index_col=0)
    n_vars, n_factors = loadings.shape
    if not (25 <= n_vars <= 45):
        fail(f"spain_efa_loadings.csv tiene {n_vars} filas — esperado entre 25-45")
    if not (5 <= n_factors <= 15):
        fail(f"spain_efa_loadings.csv tiene {n_factors} columnas — esperado entre 5-15")
except Exception as e:
    fail(f"Error leyendo spain_efa_loadings.csv: {e}")
    sys.exit(1)

# Check 3: Comunalidades sin NaN y sin 0.0
try:
    comm = pd.read_csv(COMMUNALITIES_FILE, index_col=0)
    if comm.isnull().any().any():
        nan_vars = comm.columns[comm.isnull().any()].tolist()
        fail(f"NaN en spain_efa_communalities.csv — columnas: {nan_vars}")
    zeros = (comm == 0.0).any()
    if zeros.any():
        zero_vars = comm.columns[zeros].tolist()
        fail(f"Comunalidad exactamente 0.0 en: {zero_vars}")
    min_comm = float(comm.min().min())
except Exception as e:
    fail(f"Error leyendo spain_efa_communalities.csv: {e}")
    sys.exit(1)

# Check 4: lrscale ausente de loadings
idx_lower = [str(i).lower() for i in loadings.index]
if "lrscale" in idx_lower:
    fail("lrscale ESTÁ en spain_efa_loadings.csv — es variable de validación, no puede entrar en EFA")

# Check 5: prtvt* ausente de loadings
prtvt_found = [str(i) for i in loadings.index if str(i).lower().startswith("prtvt")]
if prtvt_found:
    fail(f"Variables prtvt* en spain_efa_loadings.csv: {prtvt_found} — son de validación")

if FAILED:
    print(f"\n{len(FAILED)} check(s) fallaron.")
    sys.exit(1)

print(f"✓ EFA OK — {n_vars} variables, {n_factors} factores, comunalidad mínima: {min_comm:.3f}")
sys.exit(0)
