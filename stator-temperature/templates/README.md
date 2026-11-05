# Project instruction templates

These are optional adapters for enforcing the `stator-temp-optimizer` session gate in a target research project. They are not Skill source files. Copy or merge only the template supported by the intended Agent, and inspect existing instructions first.

| Agent | Template | Target |
| --- | --- | --- |
| Codex | `AGENTS.template.md` | Project-root `AGENTS.md` |
| Claude Code | `CLAUDE.template.md` | Project-root `CLAUDE.md` |
| Cursor | `CURSOR.template.mdc` | `.cursor/rules/stator-temp-optimizer.mdc` |
| Antigravity | `ANTIGRAVITY-rule.template.md` | `.agents/rules/stator-temp-optimizer.md` |
| Gemini CLI | `GEMINI.template.md` | Project-root `GEMINI.md` |
| DeepSeek Harness | `DSH-AGENTS.template.md` | Project-root `AGENTS.md` |

The DSH template must be installed as `AGENTS.md` because the current DSH Agent Instructions subsystem reads `AGENTS.md` and `CLAUDE.md`; it does not load this template's source filename. These templates keep conversation activation transient and research progress under the target project's local `Ablation/` directory.
