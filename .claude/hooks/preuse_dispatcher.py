"""
preuse_dispatcher.py — Único hook PreToolUse para eu-political-observatory.
Consolida: protect_raw_data (2.1) + validate_r_script (2.2) + no-verify guard (2.8).
CRITICO: stdin contention issue #42702 — solo un hook PreToolUse puede leer stdin.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# Cadena Ollama compartida entre proyectos: vive fuera del repo, asi que no se
# puede derivar de la raiz. Se resuelve bajo el home del usuario y se puede
# apuntar a otro sitio con CLAUDE_OLLAMA_CHAIN. Si no existe, dispatch_ollama()
# sale sin bloquear (niveles 1-2 son best-effort).
OLLAMA_CHAIN = os.environ.get(
    "CLAUDE_OLLAMA_CHAIN",
    str(Path.home() / "proyectos" / ".claude" / "hooks" / "ollama_chain.py"),
)
RAW_PATH = "data/raw/"
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "StrReplace"}

# Nivel 0: violaciones metodológicas deterministas (sin LLM)
_FORBIDDEN_EFA = re.compile(
    r'\b(?:fa|fa\.parallel)\s*\([^)]*\b(?:lrscale|prtvt\w*|vote)\b',
    re.IGNORECASE | re.DOTALL,
)
_FA_POOLED_DF = re.compile(
    r'\bfa\.pooled\s*\(\s*list\s*\([^)]*\b(?:data|df|datos|dataset)\w*\b',
    re.IGNORECASE,
)


def _block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=True))
    sys.exit(2)


def nivel0_r(content: str) -> None:
    if _FORBIDDEN_EFA.search(content):
        _block(
            "BLOQUEADO Nivel 0: lrscale/prtvt*/vote son variables de validacion "
            "y no deben entrar en EFA. Regla 1."
        )
    if _FA_POOLED_DF.search(content):
        _block(
            "BLOQUEADO Nivel 0: fa.pooled recibe lista de matrices de correlacion, "
            "no datasets. Regla 4."
        )


def dispatch_ollama(file_path: str, content: str) -> None:
    """Llama ollama_chain.py para niveles 1-2. Nunca bloquea por error tecnico."""
    if not os.path.exists(OLLAMA_CHAIN):
        return
    try:
        result = subprocess.run(
            ["python", OLLAMA_CHAIN, "--file", file_path, "--project", "eu_observatory"],
            input=content,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=38,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.returncode == 1:
            _block(
                "BLOQUEADO Nivel 1-2: "
                + (result.stdout[-400:] if result.stdout else "problema metodologico detectado")
            )
    except subprocess.TimeoutExpired:
        print("preuse_dispatcher: ollama_chain timeout — pasando sin validar Nivel 1-2")
    except Exception as e:
        print(f"preuse_dispatcher: ollama_chain no disponible ({e})")


def main() -> None:
    try:
        raw = sys.stdin.buffer.read()
        payload = json.loads(raw or b"{}")
    except Exception:
        payload = {}

    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})

    # 2.8 — no-verify guard
    if tool == "Bash":
        cmd = tool_input.get("command", "")
        if "--no-verify" in cmd:
            _block(
                "BLOQUEADO: --no-verify bypasea hooks de calidad ESS. "
                "Resolver el error del hook en su lugar."
            )

    if tool in WRITE_TOOLS:
        path = str(tool_input.get("file_path", "") or tool_input.get("path", "")).replace("\\", "/")

        # 2.1 — protect data/raw/
        if RAW_PATH in path:
            _block(f"BLOQUEADO: data/raw/ es read-only. tool={tool}, path={path}")

        # 2.2 — validate R scripts
        if path.endswith(".R"):
            content = (
                tool_input.get("content", "")      # Write
                or tool_input.get("new_string", "")  # Edit/StrReplace
                or ""
            )
            if content:
                nivel0_r(content)
                dispatch_ollama(path, content)

    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"preuse_dispatcher: error inesperado ({e})")
        sys.exit(0)
