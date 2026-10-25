#!/bin/sh
# Installs cc-panel and points Claude Code's status line at it.
#   curl -fsSL https://raw.githubusercontent.com/risingjerry/claude-code-panel/main/install.sh | sh
set -eu

BIN="${CC_PANEL_BIN:-$HOME/.local/bin}"
SETTINGS="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/settings.json"
SRC="https://raw.githubusercontent.com/risingjerry/claude-code-panel/main/cc-panel"

command -v python3 >/dev/null || { echo "cc-panel needs python3" >&2; exit 1; }
mkdir -p "$BIN"
if [ -f "$(dirname "$0")/cc-panel" ]; then
  cp "$(dirname "$0")/cc-panel" "$BIN/cc-panel"
else
  curl -fsSL "$SRC" -o "$BIN/cc-panel"
fi
chmod +x "$BIN/cc-panel"
echo "installed $BIN/cc-panel"

if ! command -v ccstatusline >/dev/null; then
  if command -v npm >/dev/null; then
    npm install -g ccstatusline@2.2.32
  else
    echo "note: ccstatusline not found; cc-panel will fall back to npx (slower first render)"
  fi
fi

mkdir -p "$(dirname "$SETTINGS")"
[ -f "$SETTINGS" ] && cp "$SETTINGS" "$SETTINGS.bak-cc-panel" && echo "backup: $SETTINGS.bak-cc-panel"
python3 - "$SETTINGS" "$BIN/cc-panel" <<'EOF'
import json, os, sys
path, cmd = sys.argv[1:]
data = json.load(open(path)) if os.path.exists(path) else {}
data["statusLine"] = {"type": "command", "command": cmd, "refreshInterval": 1, "padding": 0}
json.dump(data, open(path, "w"), indent=2, ensure_ascii=False)
EOF
echo "statusLine set in $SETTINGS; preview with: cc-panel --demo"
