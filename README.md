<div align="center">

# claude-code-panel

**Turn the Claude Code status line into a live, aligned dashboard panel.**

Context, 5-hour / weekly / Fable rate limits with reset countdowns, prompt-cache TTL, cost, speed and session ID — in one glance, animated while Claude works.

[![License: MIT](https://img.shields.io/badge/license-MIT-D97757.svg)](LICENSE)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-6A9BCC.svg)
![Claude Code](https://img.shields.io/badge/Claude%20Code-status%20line-D4A27F.svg)
[![GitHub stars](https://img.shields.io/github/stars/JNHFlow21/claude-code-panel?style=social)](https://github.com/JNHFlow21/claude-code-panel/stargazers)

English · [简体中文](README.zh-CN.md)

![claude-code-panel: an animated Claude Code status line panel showing context, rate limits, cache TTL and cost](docs/demo.gif)

</div>

## Why

The default Claude Code status line is one long row of loosely spaced text. **claude-code-panel** draws it as a compact three-row panel: every label and value sits on a grid, related numbers are stacked in the same column, and the panel moves only when something is happening.

- **One block, not a bar** — an accent rail ties three aligned rows together.
- **All your limits in one column** — `5H`, `WK` and `FABLE` usage bars stacked, each with a `↻` reset countdown.
- **Warns before you hit the wall** — bars turn amber at 70% and red at 90%.
- **Prompt-cache TTL countdown** — see how long the cache stays warm (green → amber → red → `cold`), so you know when the next message will be expensive.
- **Alive while Claude works** — the `✻` spins and the rail breathes while the transcript is being written; still when idle.
- **Cheap** — redraws every second in ~30 ms; the heavy computation runs only when the session state changes.
- **One file** — a single Python script, no Python dependencies.

## Install

```sh
curl -fsSL https://raw.githubusercontent.com/JNHFlow21/claude-code-panel/main/install.sh | sh
```

The installer copies `cc-panel` to `~/.local/bin`, installs [ccstatusline](https://github.com/sirmalloc/ccstatusline) if it is missing, backs up `~/.claude/settings.json` and sets:

```json
"statusLine": {
  "type": "command",
  "command": "~/.local/bin/cc-panel",
  "refreshInterval": 1,
  "padding": 0
}
```

Preview without Claude Code: `cc-panel --demo`.

<details>
<summary>Manual install</summary>

```sh
npm install -g ccstatusline@2.2.32
curl -fsSL https://raw.githubusercontent.com/JNHFlow21/claude-code-panel/main/cc-panel -o ~/.local/bin/cc-panel
chmod +x ~/.local/bin/cc-panel
```

Then add the `statusLine` block above to `~/.claude/settings.json` (use the absolute path).
</details>

## What each field means

| Field | Meaning |
|---|---|
| `✻ Opus 5.5 high` | Model and reasoning effort |
| `$3.8217  42m` | Session cost (API-price estimate, same as `/cost`) and session wall time |
| `CTX` | Context window used, with token count |
| `CACHE` | Prompt-cache hit rate |
| `TTL` | Time until the prompt cache expires |
| `5H` / `WK` / `FABLE` | 5-hour, weekly and Fable weekly usage, `↻` = time until reset |
| `OUT` | Output speed (tokens/s) |
| `TTFT` | Average wait until the first response block (an upper bound on time-to-first-token) |
| `TOOL` | Total wall time spent in tool calls (parallel calls counted once) |
| `TOK` | Total tokens this session |
| `ID` | Session ID — pass it to `claude --resume` |

## How it works

Claude Code pipes a JSON snapshot of the session to the status-line command. `cc-panel` hands it to **ccstatusline** with a generated data-only config (no colors, values separated by `␟`), reads TTFT and tool time from the session transcript incrementally, and lays everything out on a grid with true-color ANSI. ccstatusline's output is cached per session and recomputed only when the model, cost, tokens or rate limits change (or every 30 s), so the one-second refresh stays cheap.

## FAQ

**How do I customize the Claude Code status line?**
Set `statusLine.command` in `~/.claude/settings.json` to any script that reads JSON on stdin and prints text. `cc-panel` is such a script; `refreshInterval: 1` makes Claude Code re-run it every second so countdowns and animation stay live.

**Can the status line show my Claude rate limits and when they reset?**
Yes. `5H` and `WK` come straight from the `rate_limits` field Claude Code sends; `FABLE` comes from ccstatusline's usage fetch (the same source as `/usage`). Each shows a `↻` countdown to its reset.

**Why does the cache TTL matter?**
Cached prompt tokens are much cheaper. When `TTL` turns red or `cold`, the next message rebuilds the cache at full price — a good moment to send it soon or to `/compact` first.

**Can it show the permission mode (bypass / plan)?**
No. The `▶▶ bypass permissions on` row is drawn by Claude Code itself below the status line, and the permission mode is not part of the status-line JSON. The panel's text is indented to line up with that row so they read as one block.

**Does it slow Claude Code down?**
A redraw takes ~30 ms. The ~1 s ccstatusline run only happens when the session state changes, and never blocks Claude itself.

**Does it work on Linux / with other fonts?**
It needs Python 3.10+, a true-color terminal and a font with `▰ ▱ ▌ ✻ ↻` (most modern monospace fonts). Tested on macOS with Claude Code 2.1.302 and ccstatusline 2.2.32.

## Uninstall

Restore `~/.claude/settings.json.bak-cc-panel` (or remove the `statusLine` block) and delete `~/.local/bin/cc-panel` and `~/.cache/cc-panel`.

## Development

```sh
python3 -m unittest discover -s tests   # tests
python3 docs/render.py                  # regenerate docs/demo.gif and docs/screenshot.png (needs Chrome + ffmpeg)
```

## Credits

Built on [ccstatusline](https://github.com/sirmalloc/ccstatusline) by sirmalloc. Colors follow Claude Code's own palette.

---

If this made your terminal nicer, a ⭐ helps other Claude Code users find it.

[MIT](LICENSE)
