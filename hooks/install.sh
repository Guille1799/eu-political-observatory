#!/bin/bash
# Activa los hooks versionados en ESTE clon. Ver hooks/README.md.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

git config core.hooksPath hooks
chmod +x hooks/pre-commit 2>/dev/null || true

echo "✓ core.hooksPath = $(git config --get core.hooksPath)"
echo ""

# Las rutas locales que el hook necesita. Se avisa, no se bloquea: install.sh no es el guard.
VIGILANTE_REPO="$(git config --get hooks.vigilanteRepo 2>/dev/null || true)"
: "${VIGILANTE_REPO:=C:/Users/Guille/proyectos/capa-normativa}"
SECRET_SCAN="$(git config --get hooks.secretScan 2>/dev/null || true)"
: "${SECRET_SCAN:=C:/Users/Guille/proyectos/.claude/hooks/vigilante_pre_commit.py}"

if [ -d "$VIGILANTE_REPO/src/capa_normativa/vigilante" ]; then
    echo "✓ vigilante encontrado: $VIGILANTE_REPO"
else
    echo "⚠️  vigilante NO encontrado en: $VIGILANTE_REPO"
    echo "   El Check 2 usará la reserva inline (ast.parse sobre lo que esté en stage)."
    echo "   Para apuntarlo bien:  git config hooks.vigilanteRepo \"/ruta/a/capa-normativa\""
fi

if [ -f "$SECRET_SCAN" ]; then
    echo "✓ escáner de credenciales encontrado: $SECRET_SCAN"
else
    echo "❌ escáner de credenciales NO encontrado en: $SECRET_SCAN"
    echo "   El Check 3 BLOQUEARÁ todos los commits hasta que exista (es deliberado)."
    echo "   Para apuntarlo bien:  git config hooks.secretScan \"/ruta/a/vigilante_pre_commit.py\""
fi
