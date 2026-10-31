# Agent guide — claude-code-panel

A Claude Code status line drawn as an aligned, animated three-row panel. The whole product is one Python script, `cc-panel`, plus `install.sh`.

## Layout

- `cc-panel` — the status-line command (Python 3.10+, standard library only). Claude Code pipes a session JSON on stdin; it prints the panel. `cc-panel --demo` renders sample data without Claude Code.
- `install.sh` — copies `cc-panel` to `~/.local/bin`, installs `ccstatusline@2.2.32` via npm if missing, backs up `settings.json` to `settings.json.bak-cc-panel`, then sets the `statusLine` block.
- `tests/test_panel.py` — offline unit tests.
- `docs/render.py` — regenerates `docs/demo.gif` and `docs/screenshot.png` (needs Chrome + ffmpeg).
- `skills/claude-code-panel/SKILL.md` — how an agent installs, configures and removes the panel for a user.

## Test

```sh
python3 -m unittest discover -s tests
python3 cc-panel --demo        # visual smoke check, no side effects beyond ~/.cache/cc-panel
```

## How it works

ccstatusline is run with a generated data-only config; `cc-panel` reads TTFT and tool time from the session transcript incrementally and lays everything out on a grid. ccstatusline output is cached per session under `~/.cache/cc-panel` and recomputed only when model, cost, tokens or rate limits change (or every 30 s). The `FABLE` usage fetch is rate-limited to one per 15 minutes across all sessions; do not add a faster poll. The other-subscription rows (Codex, Grok, Google, DeepSeek) come from a detached `cc-panel --refresh-quotas` that holds a machine-wide lock and keeps a per-source interval with failure backoff in `~/.cache/cc-panel/quotas.json`; the panel itself only reads that file.

## Rules

- Never overwrite the user's `settings.json` without a backup; edit only the `statusLine` key and keep every other key.
- Never print or store credentials. The only credentials touched are the Grok CLI's own login (read-only, in memory) and the DeepSeek key from the user's `deepseek_key_command` (in memory); never write them anywhere or pass them on argv. The Google row runs `agy -p /usage` and never touches Antigravity's login files. Network calls are limited to the background refresh of those sources; no telemetry.
- Keep it a single dependency-free script; Python 3.10 compatible.
- Do not run the installer on a machine unless the user asked to install.
- Before changing layout code, run the tests and `cc-panel --demo` and compare.

For installing or removing the panel for a user, read `skills/claude-code-panel/SKILL.md`.
