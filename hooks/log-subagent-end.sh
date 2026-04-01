#!/bin/bash
# Hook: SubagentEnd - Actualiza la fila existente con fecha_end y duración
# Busca por session_id la fila creada por SubagentStart y la completa

LOG_FILE="/workspaces/demo-sesion/.github/hooks/subagent-log.csv"

# Read all stdin into variable
INPUT=$(cat)

# Debug: log raw input
echo "[$(date '+%Y-%m-%d %H:%M:%S')] END raw input: $INPUT" >> /workspaces/demo-sesion/.github/hooks/subagent-debug.log

# Parse fields using python3
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('sessionId','sin-session'))" 2>/dev/null || echo "sin-session")
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Actualizar la fila y capturar fecha_start del subagente
SUBAGENT_START=$(python3 << PYEOF
import csv, os
from datetime import datetime

log_file = "$LOG_FILE"
session_id = "$SESSION_ID"
fecha_end = "$TIMESTAMP"

if not os.path.exists(log_file):
    exit(0)

rows = []
updated = False
fecha_start_found = ''
with open(log_file, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header)
    for row in reader:
        # Columnas: fecha_start,fecha_end,duracion_seg,agente,agent_id,session_id,usuario
        if len(row) >= 7 and row[5] == session_id and row[1] == '':
            fecha_start_found = row[0]
            row[1] = fecha_end
            try:
                t0 = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                t1 = datetime.strptime(fecha_end, '%Y-%m-%d %H:%M:%S')
                row[2] = str(int((t1 - t0).total_seconds()))
            except:
                row[2] = ''
            updated = True
        rows.append(row)

with open(log_file, 'w', newline='') as f:
    writer = csv.writer(f, lineterminator='\n')
    writer.writerows(rows)

# Emit start timestamp for the hook to use
if fecha_start_found:
    print(fecha_start_found)
PYEOF
)

# SUBAGENT_START now contains the fecha_start from the CSV (or empty if not found)

# Parse agent_type for quick filtering
AGENT_TYPE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('agent_type','default'))" 2>/dev/null || echo "default")

# Skip report for agents that definitely don't run tests
SKIP_AGENTS="quality-sonarqube|jon-apx_doc_generator|jon-apx_html_doc_generator|skill-creator|agentic-workflows|dotnet-upgrade"
if echo "$AGENT_TYPE" | grep -qiE "^($SKIP_AGENTS)$"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] END skipping report — agent_type '$AGENT_TYPE' not a test agent" >> /workspaces/demo-sesion/.github/hooks/subagent-debug.log
else
    # For other agents (default, apx-unit-test*, etc.), check if tests actually ran
    REPORT_SCRIPT="/workspaces/demo-sesion/.github/hooks/collect_and_report.py"
    if [ -f "$REPORT_SCRIPT" ] && [ -n "$SUBAGENT_START" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] END triggering collect_and_report.py --since '$SUBAGENT_START' (agent=$AGENT_TYPE)" >> /workspaces/demo-sesion/.github/hooks/subagent-debug.log
        python3 "$REPORT_SCRIPT" --since "$SUBAGENT_START" >> /workspaces/demo-sesion/.github/hooks/subagent-debug.log 2>&1 &
    fi
fi

# REQUIRED: Return valid JSON to stdout so VS Code continues
echo '{"continue":true}'
