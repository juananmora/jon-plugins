#!/bin/bash
# Hook: Salvar contexto antes de la compactación de Copilot
# Se ejecuta en el evento PreCompact

# Leer el JSON de entrada que envía VS Code
INPUT=$(cat)

# Extraer información relevante
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // "unknown"')
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')

# Directorio donde guardar los snapshots (raíz del proyecto)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SAVE_DIR="$PROJECT_ROOT/copilot-snapshots"
mkdir -p "$SAVE_DIR"

# Guardar el input completo del evento (contiene el contexto antes de compactar)
echo "$INPUT" | jq '.' > "$SAVE_DIR/pre-compact-${TIMESTAMP}.json"

# Guardar un log resumido
LOG_FILE="$SAVE_DIR/compact-history.log"
echo "[$TIMESTAMP] Session: $SESSION_ID - Contexto salvado antes de compactar" >> "$LOG_FILE"

# Devolver JSON válido para que VS Code continúe con la compactación
echo '{"continue":true}'
