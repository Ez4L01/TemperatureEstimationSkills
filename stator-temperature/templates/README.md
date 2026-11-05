# 项目指令模板

这些模板用于在科研项目中强化 `stator-temp-optimizer` 的会话级激活规则，不是 Skill 源文件，也不是安装执行型 Skill 的必需条件。请先检查目标项目已有的指令，再选择适用于目标 Agent 的模板进行复制或合并；不要直接覆盖现有文件。

| Agent | 模板 | 目标位置 |
| --- | --- | --- |
| OpenAI Codex | `AGENTS.template.md` | 项目根目录 `AGENTS.md` |
| Claude Code | `CLAUDE.template.md` | 项目根目录 `CLAUDE.md` |
| Cursor | `CURSOR.template.mdc` | `.cursor/rules/stator-temp-optimizer.mdc` |
| Google Antigravity | `ANTIGRAVITY-rule.template.md` | `.agents/rules/stator-temp-optimizer.md` |
| Gemini CLI | `GEMINI.template.md` | 项目根目录 `GEMINI.md` |
| DeepSeek Harness | `DSH-AGENTS.template.md` | 项目根目录 `AGENTS.md` |

DeepSeek Harness 的当前 Agent Instructions 默认读取 `AGENTS.md` 和 `CLAUDE.md`，因此 DSH 模板安装时应以 `AGENTS.md` 为目标文件名。请按[安装指南](../../docs/installation.md)确认对应 Agent 的调用入口和验证状态。

所有模板将会话激活状态设为临时状态，并要求实验进度保存在科研项目本地的 `Ablation/`。实验记录可跨对话保留，但不得据此自动启用新对话中的 Skill。
