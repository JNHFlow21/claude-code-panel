# Changelog

## 0.1.0 — 2026-10-25

First public release.

- Three-row aligned Claude Code status-line panel: model and effort, cost and session time, context, cache hit rate, prompt-cache TTL countdown, output speed, TTFT, tool time, tokens and session ID.
- `5H`, `WK` and `FABLE` usage bars with reset countdowns; amber at 70%, red at 90%.
- Animation while Claude works; redraw every second in about 30 ms, with ccstatusline output cached per session.
- The `FABLE` usage fetch is limited to one per 15 minutes across all sessions, which stops usage-API rate limits when many sessions are open.
- `install.sh`: one-line installer that backs up `settings.json` before setting `statusLine`; `cc-panel --demo` previews without Claude Code.
- Bundled agent skill (`skills/claude-code-panel`), unit tests and CI on Python 3.10 and 3.13.
