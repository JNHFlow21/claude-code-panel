# Changelog

## Unreleased

- `CTX` is measured against the auto-compact window (`autoCompactWindow` setting or `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, read on every redraw), so 100% means compaction is due; without one it falls back to the model window.

## 0.2.0 — 2026-10-26

- Other subscriptions under the panel, one brand-colored row each: Codex weekly usage and rate-limit reset credits (`GPT`), the X / Grok weekly pool split by product (`Grok`), and the DeepSeek balance (`DeepSeek`, opt-in via `deepseek_key_command`).
- Background refresh with a machine-wide lock, per-source intervals (5 / 10 / 15 min) and failure backoff up to 1 h; stale values grey out.
- `cc-panel --toggle` hides or shows the block; `extras/raycast` script command for a global hotkey.

## 0.1.0 — 2026-10-25

First public release.

- Three-row aligned Claude Code status-line panel: model and effort, cost and session time, context, cache hit rate, prompt-cache TTL countdown, output speed, TTFT, tool time, tokens and session ID.
- `WK` and `FABLE` usage bars with reset countdowns; amber at 70%, red at 90%.
- Animation while Claude works; redraw every second in about 30 ms, with ccstatusline output cached per session.
- The `FABLE` usage fetch is limited to one per 15 minutes across all sessions, which stops usage-API rate limits when many sessions are open.
- `install.sh`: one-line installer that backs up `settings.json` before setting `statusLine`; `cc-panel --demo` previews without Claude Code.
- Bundled agent skill (`skills/claude-code-panel`), unit tests and CI on Python 3.10 and 3.13.
