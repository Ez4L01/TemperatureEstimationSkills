# Installation and Agent compatibility

This guide was checked against the current official Agent documentation on 2026-11-06 and Skills CLI 1.7.6. The shared source is stored once under `stator-temperature/.agents/skills/`; use the repository home URL when installing.

## Discover and install

```bash
REPO=https://github.com/Ez4L01/TemperatureEstimationSkills

# Discover every Skill in the repository
npx skills add "$REPO" --list

# Install either Skill in the current project
npx skills add "$REPO" --skill stator-temp-optimizer
npx skills add "$REPO" --skill stator-temp-prompts
```

The CLI's `--list` and `--skill` options are supported by the current command help. Its project-level install is the default. Use `--global` for user-level installation and `--agent <id>` to select a supported Agent. `--copy --yes` performs a non-interactive copy. The CLI may create an additional common `.agents/skills` copy when an Agent has more than one supported skill location.

Supported target IDs verified in the current CLI's agent list:

| Agent | `--agent` ID | Project skill path | Explicit use |
| --- | --- | --- | --- |
| OpenAI Codex | `codex` | `.agents/skills/` | `$stator-temp-optimizer` or `$stator-temp-prompts` |
| Claude Code | `claude-code` | `.claude/skills/` | `/stator-temp-optimizer` or `/stator-temp-prompts` |
| Cursor | `cursor` | `.agents/skills/` | `/` then select the Skill; a manual invocation attaches to one message. |
| Google Antigravity | `antigravity` | `.agents/skills/` | `/stator-temp-optimizer`; use `/skills reload` after an in-session install. |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | Use a clear natural-language request naming the Skill; `/skills list` and `/skills reload` manage discovery. The current official skill guide documents `/skills` management commands, not `/stator-temp-optimizer`. |
| DeepSeek Harness | No native CLI ID listed | `.agents/skills/` via `universal` | `/stator-temp-optimizer` when DSH's Skill loader is available. |

The `skills` command supports additional Agent Skills targets beyond these six. Check its current [supported Agents](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) page and `npx skills add --help` before using a target ID; do not assume an undocumented identifier.

## DeepSeek Harness (DSH)

The current Skills CLI agent list does not include DSH. Do not pass an assumed `--agent deepseek-harness`. To install the selected Skill from the repository home URL into the DSH-compatible project root, use the CLI's documented `universal` target:

```bash
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer --agent universal --copy --yes
```

Verify the result is a direct child bundle:

```text
<project>/.agents/skills/stator-temp-optimizer/SKILL.md
<project>/.agents/skills/stator-temp-optimizer/references/research-execution-spec.md
```

The current DSH filesystem provider scans project `.agents/skills` after `.dsh/skills`; each Skill is a directory bundle under the scanned root. Use only one version of this Skill in the project. A same-name copy under `.dsh/skills` has higher priority and can shadow the `.agents/skills` copy.

When DSH has the filesystem provider, Skill registry, and Tool Skill consumer enabled, inspect the Skill catalog and load it by name. DSH also supports direct user invocation as `/stator-temp-optimizer`. This is a Skill load/explicit invocation; it is not itself a request to train. The DSH project-instruction subsystem currently loads `AGENTS.md` and `CLAUDE.md`, so install [AGENTS.template.md](../stator-temperature/templates/AGENTS.template.md) as the research project's `AGENTS.md`, or use [DSH-AGENTS.template.md](../stator-temperature/templates/DSH-AGENTS.template.md). Do not install a persistent `ACTIVE` flag.

This workspace does not have a `dsh` executable, so native catalog discovery and live loading were not runtime-tested. The path and invocation guidance below is based on the current [DSH Skill subsystem](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md), [filesystem provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md), [Tool Skill consumer](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.md), and [Agent Instructions subsystem](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/context/agent-instructions/README.md).

## Optional project instruction templates

Templates strengthen the session gate in a target research project; they are not required to install the Skill. Copy or merge them deliberately. Never replace existing project instructions automatically.

| Agent | Template | Install destination in target project |
| --- | --- | --- |
| Codex | [AGENTS.template.md](../stator-temperature/templates/AGENTS.template.md) | Merge into `AGENTS.md` |
| Claude Code | [CLAUDE.template.md](../stator-temperature/templates/CLAUDE.template.md) | Merge into `CLAUDE.md` |
| Cursor | [CURSOR.template.mdc](../stator-temperature/templates/CURSOR.template.mdc) | `.cursor/rules/stator-temp-optimizer.mdc` |
| Antigravity | [ANTIGRAVITY-rule.template.md](../stator-temperature/templates/ANTIGRAVITY-rule.template.md) | `.agents/rules/stator-temp-optimizer.md` |
| Gemini CLI | [GEMINI.template.md](../stator-temperature/templates/GEMINI.template.md) | Merge into `GEMINI.md` |
| DeepSeek Harness | [DSH-AGENTS.template.md](../stator-temperature/templates/DSH-AGENTS.template.md) | Merge into project-root `AGENTS.md` |

## Session activation behavior

The optimizer Skill starts `INACTIVE` in every new conversation. Neither installation, catalog discovery, listing, reading the skill, nor merely invoking it to inspect its instructions runs training or enables the standalone shortcut.

For Codex, activate with:

```text
使用 $stator-temp-optimizer，启用本次会话的迭代模式。
```

For other Agents, use their official Skill invocation (where supported) with an explicit enable request, or send:

```text
启用 stator-temp-optimizer Skill。
```

The activation turn checks that the full execution specification can be read and that the open project is suitable; it does not train. After activation, send exactly `迭代` to start or continue optimization. `退出迭代模式` or `停用 stator-temp-optimizer` returns the current conversation to `INACTIVE`. A new conversation needs fresh activation. If the Agent cannot reliably establish the current conversation state, it must fail closed and ask for activation again.

The experiment state and checkpoints are separate durable project data under `Ablation/`. They survive deactivation and can be resumed in a later conversation after explicit re-activation. They never activate the Skill. Model code and research results stay local by default; remote synchronization requires a separate explicit request.

Platform controls differ. For example, Cursor manual Skill invocation attaches to one message unless kept active in a Custom Mode; Gemini CLI documents `/skills list` and `/skills reload` plus activation consent; Antigravity supports slash commands; Claude Code and DSH have their own invocation systems. Follow the platform's own docs and the templates above. The conversation-level gate is prompt policy and does not replace host permission controls.

## Update, inspect, and remove

```bash
npx skills list
npx skills update
npx skills update stator-temp-optimizer
npx skills remove stator-temp-optimizer
```

Use `--global` with supported commands if the Skill was installed at user scope. For Gemini CLI's own manager, see its [official Agent Skills guide](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md); for this multi-Skill repository layout, the tested repository-home installation route is `npx skills`.

## Compatibility and test results

Validated locally on 2026-11-06:

| Check | Result |
| --- | --- |
| `npx skills add <repository-home-url> --list` | Passed; found `stator-temp-prompts` and `stator-temp-optimizer` from the current nested topic layout. |
| Install `stator-temp-optimizer` by name from the home URL | Passed in an isolated temporary project; default Codex detection and `universal` target placed the complete bundle under `.agents/skills/stator-temp-optimizer/`. |
| Install `stator-temp-prompts` by name from the home URL | Passed in an isolated temporary project under `.agents/skills/stator-temp-prompts/`. |
| Multi-target CLI install to Codex, Claude Code, Cursor, Antigravity, and Gemini CLI | Passed using their current supported IDs. CLI produced `.agents/skills/` and `.claude/skills/` copies; file contents matched the source after line-ending normalization. |
| Standard metadata and relative references | Verified with CLI discovery, source checks, and the repository compatibility tests. |
| Activation gate | Simulated without training by `python -m unittest discover -s stator-temperature/tests -v`. |
| Native Agent runtimes | Not runtime-tested: `dsh`, `claude`, `cursor`, `gemini`, and `agy` executables are unavailable in this workspace. |
| Training | Not run. |

The native `.agents/skills` installation layout is compatible with the published directory rules for Codex, Cursor, Antigravity, Gemini CLI, DSH, and the open standard. Claude Code's CLI target installs to `.claude/skills`; its references remain within the same skill folder.

## Official references

- [Agent Skills specification](https://agentskills.io/specification)
- [Skills CLI commands](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) and [supported Agent paths](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
- [Codex Skills](https://developers.openai.com/codex/skills)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- [Cursor Skills](https://cursor.com/docs/skills) and [project rules](https://cursor.com/docs/rules)
- [Antigravity Skills](https://antigravity.google/docs/skills), [rules](https://antigravity.google/docs/rules), and [customization discovery](https://antigravity.google/docs/customization-discovery)
- [Gemini CLI Agent Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md) and [GEMINI.md context](https://geminicli.com/docs/cli/gemini-md/)
- [DSH Skill subsystem](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)
