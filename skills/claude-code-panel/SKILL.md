---
name: claude-code-panel
description: Install, configure or remove claude-code-panel, a Claude Code status line that shows context, 5-hour / weekly rate limits with reset countdowns, prompt-cache TTL, cost and session ID as an aligned animated panel. Use when the user wants a better Claude Code status line, wants to see rate limits or cache TTL in the terminal, mentions cc-panel or ccstatusline, or wants the panel removed. 状态栏 / 用量面板 / 限额倒计时.
---

# claude-code-panel

A Claude Code `statusLine` command (`cc-panel`) that draws a three-row live panel. It changes the user's Claude Code settings, so confirm before installing.

## First contact

```sh
command -v cc-panel && cc-panel --demo     # already installed? preview it
python3 --version                          # needs 3.10+
```

Requirements: Python 3.10+, a true-color terminal, `npm` (for ccstatusline; without it the panel falls back to a slower `npx`).

## Install

Tell the user it will edit `~/.claude/settings.json` (backed up first), then run:

```sh
curl -fsSL https://raw.githubusercontent.com/risingjerry/claude-code-panel/main/install.sh | sh
```

It copies `cc-panel` to `~/.local/bin`, installs `ccstatusline@2.2.32` if missing, saves `~/.claude/settings.json.bak-cc-panel`, and sets only the `statusLine` key:

```json
"statusLine": {"type": "command", "command": "~/.local/bin/cc-panel", "refreshInterval": 1, "padding": 0}
```

Then run `cc-panel --demo` to show the preview and tell the user to restart Claude Code (or open a new session). Env overrides: `CC_PANEL_BIN` (install dir), `CLAUDE_CONFIG_DIR` (settings location).

## Manual install (if piping curl to sh is not acceptable)

```sh
npm install -g ccstatusline@2.2.32
curl -fsSL https://raw.githubusercontent.com/risingjerry/claude-code-panel/main/cc-panel -o ~/.local/bin/cc-panel
chmod +x ~/.local/bin/cc-panel
```

Then back up `~/.claude/settings.json` and add the `statusLine` block above, using an absolute path. Keep all other keys.

## Safety rules

- Always back up `settings.json` before editing and never drop other keys.
- If `statusLine` already points at another command, show it to the user and ask before replacing; mention how to restore.
- Do not install system-wide packages other than `ccstatusline` via npm.

## Reading the panel

`5H` / `WK` / `FABLE` = usage bars with `↻` time to reset (amber at 70%, red at 90%); `TTL` = prompt-cache time left (red or `cold` means the next message is full price); `CTX` = context used; `ID` = session id for `claude --resume`. The permission-mode row (`bypass permissions`) is drawn by Claude Code itself and cannot be shown by the panel.

## Troubleshooting

- Blank or garbled panel: font lacks `▰ ▱ ▌ ✻ ↻`, or the terminal is not true-color. Run `cc-panel --demo` outside Claude Code to compare.
- `GPT` / `Grok` / `DeepSeek` rows missing: the matching CLI (`codex`, `grok`) is not logged in, or DeepSeek has no `deepseek_key_command` in `~/.config/cc-panel/config.json` (a command that writes the key to fd 3; never put the key itself there). Grey = stale value, refreshed in the background. `cc-panel --toggle` hides or shows them; `CC_PANEL_QUOTAS=0` disables them.
- `FABLE` row missing or stale: the usage API is rate-limited and fetched at most every 15 minutes; wait.
- First render slow: ccstatusline missing, so `npx` is used. Run `npm install -g ccstatusline@2.2.32`.

## Uninstall

```sh
cp ~/.claude/settings.json.bak-cc-panel ~/.claude/settings.json   # or delete only the statusLine block
rm ~/.local/bin/cc-panel && rm -rf ~/.cache/cc-panel
```

Restoring the backup also reverts any settings changed after install; if unsure, remove just the `statusLine` key instead.
