"""
stop_gate_eu.py — Stop hook para eu-political-observatory.
Anti-loop guard + hard cap + verificacion de integridad EFA.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ITER_FILE = Path(tempfile.gettempdir()) / "claude_stop_gate_eu_iter"
MAX_ITER = 3
# .claude/hooks/stop_gate_eu.py -> raiz del repo. Derivado del propio fichero
# para que funcione en cualquier clon o worktree, no solo en una maquina.
PROJECT_DIR = str(Path(__file__).resolve().parents[2])
EFA_LOADINGS = os.path.join(PROJECT_DIR, "data", "processed", "ess", "spain",
                            "spain_efa_loadings.csv")


def _block(reason: str, context: str = "") -> None:
    print(json.dumps({
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "Stop",
            "additionalContext": context or reason,
        },
    }, ensure_ascii=True))
    sys.exit(0)


def main() -> None:
    try:
        raw = sys.stdin.buffer.read()
        payload = json.loads(raw) if raw else {}
    except Exception:
        payload = {}

    # Anti-loop: si ya estamos en un stop hook activo, salir
    if payload.get("stop_hook_active"):
        sys.exit(0)

    # Hard cap: max MAX_ITER iteraciones por sesion
    try:
        count = int(ITER_FILE.read_text().strip()) if ITER_FILE.exists() else 0
    except Exception:
        count = 0

    if count >= MAX_ITER:
        print(f"stop_gate_eu: max iteraciones ({MAX_ITER}) alcanzadas — saliendo sin bloquear")
        try:
            ITER_FILE.unlink(missing_ok=True)
        except Exception:
            pass
        sys.exit(0)

    try:
        ITER_FILE.write_text(str(count + 1))
    except Exception:
        pass

    # Si no hay outputs EFA no hay nada que verificar
    if not os.path.exists(EFA_LOADINGS):
        sys.exit(0)

    # EFA ejecutada — verificar integridad
    check_script = os.path.join(PROJECT_DIR, "eval", "check_efa_output.py")
    if not os.path.exists(check_script):
        sys.exit(0)

    try:
        result = subprocess.run(
            ["python", check_script],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.returncode != 0:
            _block(
                "check_efa_output.py detecto problemas en el pipeline EFA.",
                (result.stdout or "") + (result.stderr or ""),
            )
        sys.exit(0)
    except subprocess.TimeoutExpired:
        print("advertencia: check_efa_output.py timeout — revisar manualmente")
        sys.exit(0)
    except Exception as e:
        print(f"advertencia: stop_gate_eu no disponible ({e})")
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"stop_gate_eu: error inesperado ({e})")
        sys.exit(0)
