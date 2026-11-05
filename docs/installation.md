# 安装与 Agent 兼容说明

本文说明如何从仓库首页安装 `stator-temp-optimizer`，以及各 Agent 的项目级路径、调用入口和验证状态。仓库目前只有这一个可安装 Skill；[科研提示词资料库](../stator-temperature/prompts/index.md)是普通 Markdown 文档，不需要安装。

CLI 命令和 Agent 目标列表于 2026-11-06 使用 Skills CLI 1.7.6 检查。平台原生运行情况单独列出，不能以文件安装成功代替原生 Agent 验证。

## 从仓库首页发现和安装

安装需要 Node.js 与 npm 提供的 `npx`。建议在目标科研项目目录执行，默认安装为项目级 Skill：

```bash
# 查看仓库中可安装的 Skill
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --list

# 按名称安装唯一的执行型 Skill
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer
```

不提供 `--agent` 时，CLI 使用当前环境的 Agent 检测与默认安装方式。指定 `--agent <id>` 可选择受支持的目标；`--copy --yes` 表示复制文件并跳过交互确认。项目安装是默认行为，`--global` 用于用户级安装。请勿把用户级安装误认为项目级安装。

当前 CLI 文档列出的相关 Agent 标识及项目路径如下。不同版本可能变化，使用前可运行 `npx skills add --help` 并查阅[当前支持的 Agent 列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。

| Agent | CLI 标识 | 项目级路径 | 建议的 Skill 调用入口 |
| --- | --- | --- | --- |
| OpenAI Codex | `codex` | `.agents/skills/` | `$stator-temp-optimizer`，并明确要求启用或执行 |
| Claude Code | `claude-code` | `.claude/skills/` | `/stator-temp-optimizer`，随后明确要求启用或执行 |
| Cursor | `cursor` | `.agents/skills/` | 使用 `/` 菜单选择 Skill；按需将其用于当前消息 |
| Google Antigravity | `antigravity` | `.agents/skills/` | `/stator-temp-optimizer`，随后明确要求启用或执行 |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | 在交互界面使用 `/stator-temp-optimizer` 并明确请求启用；`/skills list` 与 `/skills reload` 用于管理目录 |
| DeepSeek Harness（DSH） | 无专用标识 | `.agents/skills/`，通过 `universal` | 从已启用的 Skill Catalog 使用 `skill` 工具按名称加载；官方资料未说明 `/stator-temp-optimizer` 斜杠命令 |

Skills CLI 还支持其他 Agent。只有当前 CLI 文档或 `--help` 明确列出的标识才可使用，不要自行猜测 Agent ID。

## DeepSeek Harness（DSH）

当前 Skills CLI 的支持列表中没有 DSH 专用目标。使用 CLI 的通用 `universal` 目标，将 Skill 安装到项目中的标准 `.agents/skills/` 目录：

```bash
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer --agent universal --copy --yes
```

安装后应是直接子目录，而非额外嵌套：

```text
<project>/.agents/skills/stator-temp-optimizer/SKILL.md
<project>/.agents/skills/stator-temp-optimizer/references/research-execution-spec.md
```

当前 DSH 本地文件系统 Provider 扫描项目级 `.dsh/skills/` 与 `.agents/skills/`；前者优先级更高，并且 Provider 只发现扫描根目录下的直接 Skill 条目，不递归搜索嵌套的 `SKILL.md`。因此建议使用上述 `.agents/skills/stator-temp-optimizer/`，且避免在 `.dsh/skills/` 放置另一个同名版本，以免它遮蔽此安装。

DSH 运行环境还必须加载本地 Skill filesystem Provider、Skill registry 和模型侧 Skill consumer。可在运行时的 Skill Catalog 中查找并通过 `skill` 工具按名称加载。官方文档描述了该工具和目录发现机制，但没有说明 `/stator-temp-optimizer` 斜杠命令；本仓库也没有 DSH 可执行程序，因此 DSH 原生发现、加载和调用尚未在本机实测。加载 Skill 只会提供指令，不代表已开始训练。

DSH 当前 Agent Instructions 文档将项目根目录的 `AGENTS.md` 和 `CLAUDE.md` 列为默认候选文件。需要加强会话激活规则时，可将 [AGENTS.template.md](../stator-temperature/templates/AGENTS.template.md) 或 [DSH-AGENTS.template.md](../stator-temperature/templates/DSH-AGENTS.template.md) 检查后合并到项目 `AGENTS.md`。不要覆盖目标项目已有的指令文件。

机制依据：[DSH Skills 子系统](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)、[本地文件系统 Provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md)、[Agent Instructions](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/context/agent-instructions/README.md)。

## 可选的项目指令模板

以下模板用于目标科研项目，不属于 Skill 安装包。请先查看目标文件，只在确认适用后手动复制或合并；不要自动覆盖已有项目规则。

| Agent | 模板 | 目标项目中的文件 |
| --- | --- | --- |
| OpenAI Codex | [AGENTS.template.md](../stator-temperature/templates/AGENTS.template.md) | 合并到项目根目录 `AGENTS.md` |
| Claude Code | [CLAUDE.template.md](../stator-temperature/templates/CLAUDE.template.md) | 合并到项目根目录 `CLAUDE.md` |
| Cursor | [CURSOR.template.mdc](../stator-temperature/templates/CURSOR.template.mdc) | `.cursor/rules/stator-temp-optimizer.mdc` |
| Google Antigravity | [ANTIGRAVITY-rule.template.md](../stator-temperature/templates/ANTIGRAVITY-rule.template.md) | `.agents/rules/stator-temp-optimizer.md` |
| Gemini CLI | [GEMINI.template.md](../stator-temperature/templates/GEMINI.template.md) | 合并到项目根目录 `GEMINI.md` |
| DeepSeek Harness | [DSH-AGENTS.template.md](../stator-temperature/templates/DSH-AGENTS.template.md) | 合并到项目根目录 `AGENTS.md` |

模板只用于强化当前对话的激活规则，不保存跨会话的 `ACTIVE` 状态。更多说明见[模板索引](../stator-temperature/templates/README.md)。

## 会话级激活与调用

每个新对话中的 Skill 状态都是 `INACTIVE`。安装、发现、列出或阅读 Skill 都不会激活迭代模式，也不会启动模型训练。

在 Codex 中，可在当前对话发送：

```text
使用 $stator-temp-optimizer，启用本次会话的迭代模式。
```

其他 Agent 可使用其正式支持的 Skill 调用入口，并明确发送：

```text
启用 stator-temp-optimizer Skill。
```

启用时应读取 `SKILL.md` 和完整科研执行规范，并检查项目是否适合执行；启用本身不运行训练。确认当前对话已经启用后，单独发送 `迭代` 才开始或继续优化。发送 `退出迭代模式` 或 `停用 stator-temp-optimizer` 后，快捷口令停止生效。新对话须重新启用；若 Agent 无法可靠确认当前激活状态，应要求用户重新启用。

不同平台可能将 Skill 调用实现为命令、菜单选择、Catalog 或模型工具。Gemini CLI 的 `/skills enable <name>` 用于更改 Skill 的可用状态，不等同于本 Skill 的会话级启用；请在当前对话中明确要求启用迭代模式。Gemini CLI 官方指南还要求 Skill 被触发时征求激活许可。会话激活规则由 Skill 指令约束，Agent 对自然语言状态的遵循能力可能不同；可将对应项目模板合并到项目说明中。平台的文件和终端权限仍由宿主控制。

实验状态和会话状态分开保存。模型与实验进度位于科研项目本地的 `Ablation/`，可以在后续对话中恢复；已保存的实验记录不能作为新对话自动激活的依据。实验默认不上传，GitHub 同步需另行得到用户明确授权。

## 更新、检查和卸载

在安装 Skill 的项目目录中运行：

```bash
# 查看项目级已安装 Skill
npx skills list

# 更新全部 Skill 或仅更新本 Skill
npx skills update
npx skills update stator-temp-optimizer

# 移除项目级 Skill
npx skills remove stator-temp-optimizer
```

若安装在用户级，请按 CLI 支持情况为相应命令添加 `--global`。Gemini CLI 也提供自己的 Skill 管理命令，详见其[官方 Agent Skills 指南](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md)。针对本仓库的专题目录结构，`npx skills` 是已检查的发现和安装方式。

提示词资料库是[普通 Markdown 文档](../stator-temperature/prompts/index.md)，请直接浏览或读取，不要通过 Skills CLI 安装。若其他科研项目此前安装了已移除的 `stator-temp-prompts` Skill，本仓库不会替用户自动卸载；请在对应项目中运行 `npx skills remove stator-temp-prompts`，或使用该 Agent 的 Skill 管理功能手动清理。

## 兼容性与测试记录

以下区分本地仓库结构、CLI 文件安装和 Agent 原生运行。记录日期：2026-11-06。

| 检查项 | 结果 |
| --- | --- |
| Skills CLI 版本及参数 | 本机 `npx skills --version` 为 1.7.6；`npx skills add --help` 确认支持 `--list`、`--skill`、`--agent`、`--copy`、`--yes`、`--global`，以及项目默认安装。 |
| 本地仓库首页发现 | 通过 `npx skills add . --list` 实测，仅发现 `stator-temp-optimizer`。 |
| 按名称安装本地 Skill | 在隔离的临时项目中从本地源按名称安装成功；安装所得 `SKILL.md` 与 `research-execution-spec.md` 和源文件内容一致（忽略换行格式差异）。 |
| Codex、Claude Code、Cursor、Antigravity、Gemini CLI 的 CLI 目标路径 | 先前使用 CLI 支持的目标标识完成复制安装检查，文件内容与源文件一致；这只验证 CLI 路径和文件复制。 |
| 修改后 GitHub 仓库首页 URL | 尚未检查。当前仓库改动仍在本地，远程 URL 仍代表尚未更新的版本，因此不能将远程结果当作本次修改后的验证。 |
| Skill 元数据和相对引用 | 本地静态检查与仓库兼容性测试通过。 |
| 会话级激活逻辑 | 通过不启动训练的状态模拟测试。 |
| DSH 原生发现、加载和调用 | 未实测；当前工作区无 `dsh` 可执行程序。目录与接口说明依据上方官方资料检查。 |
| 其他 Agent 原生运行 | 未在宿主运行时逐一实测；CLI 文件安装不能代表已完成原生调用测试。 |
| 神经网络训练 | 未运行。 |

## 官方资料

- [Agent Skills 开放规范](https://agentskills.io/specification)
- [Skills CLI 命令](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)与[支持的 Agent 和安装路径](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
- [OpenAI Codex Skills](https://developers.openai.com/codex/skills)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Cursor Skills](https://cursor.com/docs/skills)与[项目规则](https://cursor.com/docs/rules)
- [Google Antigravity Skills](https://antigravity.google/docs/skills)、[规则](https://antigravity.google/docs/rules)和[自定义资源发现](https://antigravity.google/docs/customization-discovery)
- [Gemini CLI Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md)与[`GEMINI.md` 上下文说明](https://geminicli.com/docs/cli/gemini-md/)
- [DeepSeek Harness Skills 子系统](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
