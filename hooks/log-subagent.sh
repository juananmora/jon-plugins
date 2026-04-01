#!/bin/bash
# Hook: SubagentStart - Crea fila en CSV con fecha_start

LOG_FILE="/workspaces/demo-sesion/.github/hooks/subagent-log.csv"
LOCK_FILE="/workspaces/demo-sesion/.github/hooks/.subagent-start.lock"

# Read all stdin into variable
INPUT=$(cat)

# Debug: log raw input
echo "[$(date '+%Y-%m-%d %H:%M:%S')] START raw input: $INPUT" >> /workspaces/demo-sesion/.github/hooks/subagent-debug.log

# Prevent duplicate execution (VS Code fires SubagentStart twice)
CURRENT_HASH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); d.pop('timestamp',None); print(sorted(d.items()))" 2>/dev/null | md5sum | cut -d' ' -f1)
if [ -f "$LOCK_FILE" ]; then
  PREV_HASH=$(cat "$LOCK_FILE")
  if [ "$CURRENT_HASH" = "$PREV_HASH" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SKIP duplicate start" >> /workspaces/demo-sesion/.github/hooks/subagent-debug.log
    echo '{"continue":true}'
    exit 0
  fi
fi
echo "$CURRENT_HASH" > "$LOCK_FILE"

# Parse fields using python3
AGENT_TYPE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('agent_type','desconocido'))" 2>/dev/null || echo "desconocido")
AGENT_ID=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('agent_id','sin-id'))" 2>/dev/null || echo "sin-id")
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sessionId','sin-session'))" 2>/dev/null || echo "sin-session")
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
USER=$(git config user.name 2>/dev/null || whoami)

# Crear cabecera si el archivo no existe
if [ ! -f "$LOG_FILE" ]; then
  echo "fecha_start,fecha_end,duracion_seg,agente,agent_id,session_id,usuario" > "$LOG_FILE"
fi

# Crear nueva fila con fecha_start (SubagentStop se encarga de rellenar fecha_end)
echo "$TIMESTAMP,,,${AGENT_TYPE},${AGENT_ID},${SESSION_ID},${USER}" >> "$LOG_FILE"

# REQUIRED: Return valid JSON to stdout so VS Code continues
echo '{"continue":true}'
