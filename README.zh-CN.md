<div align="center">

# claude-code-panel

**把 Claude Code 的状态栏变成一块对齐、会动的实时面板。**

上下文、5 小时 / 每周 / Fable 额度和重置倒计时、提示缓存剩余时间、花费、输出速度、会话 ID，一眼看完；Claude 干活时面板会动。

[English](README.md) · 简体中文

![claude-code-panel：会动的 Claude Code 状态栏面板，显示上下文、额度、缓存剩余时间和花费](docs/demo.gif)

</div>

## 特点

- **是一块，不是一条**：左侧色条把三行对齐的信息连成一个整体。
- **额度放一列**：`5H`、`WK`、`FABLE` 三根格子条上下叠放，后面跟 `↻` 重置倒计时。
- **快满了会提醒**：超过 70% 变琥珀色，超过 90% 变红。
- **缓存倒计时**：`TTL` 显示提示缓存还剩多久过期（绿 → 琥珀 → 红 → `cold`），过期后下一条消息会贵很多。
- **干活时会动**：Claude 工作时 `✻` 转圈、色条呼吸；空闲时静止。
- **很轻**：每秒重画一次只要约 30 毫秒，重计算只在会话数据变化时才跑。
- **一个文件**：单个 Python 脚本，不需要额外的 Python 依赖。

## 安装

```sh
curl -fsSL https://raw.githubusercontent.com/JNHFlow21/claude-code-panel/main/install.sh | sh
```

安装脚本会把 `cc-panel` 放到 `~/.local/bin`，没有 [ccstatusline](https://github.com/sirmalloc/ccstatusline) 时自动安装，先备份 `~/.claude/settings.json` 再写入 `statusLine` 配置（`refreshInterval: 1`）。不开 Claude Code 也能预览：`cc-panel --demo`。

## 各项含义

| 字段 | 含义 |
|---|---|
| `✻ Opus 5.5 high` | 模型和推理档位 |
| `$3.8217  42m` | 本次会话花费（按 API 价格估算，和 `/cost` 一致）和时长 |
| `CTX` | 上下文占用和 token 数 |
| `CACHE` | 提示缓存命中率 |
| `TTL` | 提示缓存还剩多久过期 |
| `5H` / `WK` / `FABLE` | 5 小时、每周、Fable 每周额度；`↻` 后是距离重置的时间 |
| `OUT` | 输出速度（token/秒） |
| `TTFT` | 平均首段等待时间（首个 token 时间的上限） |
| `TOOL` | 工具调用总耗时（并行调用只算一次） |
| `TOK` | 本次会话累计 token |
| `ID` | 会话 ID，可用于 `claude --resume` |

## 常见问题

**能不能显示权限模式（bypass / plan）？** 不能。`▶▶ bypass permissions on` 那一行是 Claude Code 自己画在状态栏下面的，状态栏收到的数据里也没有权限模式。面板文字已经和那一行对齐，看起来是一个整体。

**会不会拖慢 Claude Code？** 不会。重画一次约 30 毫秒，约 1 秒的 ccstatusline 计算只在数据变化时运行，也不会阻塞 Claude 本身。

## 卸载

恢复 `~/.claude/settings.json.bak-cc-panel`（或删掉 `statusLine` 配置），再删除 `~/.local/bin/cc-panel` 和 `~/.cache/cc-panel`。

---

觉得好用的话，点个 ⭐ 能让更多 Claude Code 用户看到它。

[MIT](LICENSE)
