# Security policy

## Supported versions

The latest `main` and the latest tagged release.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting
([report here](https://github.com/risingjerry/claude-code-panel/security/advisories/new))
instead of a public issue. Expect a first reply within a week.

## Threat model in short

- `cc-panel` runs as a Claude Code status-line command with your user's permissions. It reads the session JSON and transcript Claude Code gives it and keeps caches in `~/.cache/cc-panel`; it sends nothing anywhere.
- The `FABLE` usage figure comes from ccstatusline's usage fetch, which uses Claude Code's own login; `cc-panel` itself never reads or stores credentials.
- `install.sh` modifies only the `statusLine` key of `~/.claude/settings.json` after saving a backup. Read it before piping it to `sh`.
