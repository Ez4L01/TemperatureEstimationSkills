# Stator Temperature Project Instructions

Use this template only when deliberately copied or merged into a research project's `CLAUDE.md`. These instructions apply to this project and do not change Claude Code's user-level settings. The optimizer is an execution Skill; research prompts are ordinary Markdown documents.

## Session gate for `stator-temp-optimizer`

- Start every new Claude Code conversation `INACTIVE`. Skill discovery, `/stator-temp-optimizer`, or reading its files only loads instructions; it does not activate the iteration shortcut or start training.
- Activate only after the user clearly sends `启用 stator-temp-optimizer Skill。` or `/stator-temp-optimizer 启用迭代模式` in the current conversation.
- Treat mentions or quoted examples as ordinary text, not activation.
- Only while this conversation is `ACTIVE`, and only when the latest user message trimmed of surrounding whitespace is exactly `迭代`, may the optimizer run. Otherwise, do not inspect or change the research project and reply: `当前对话尚未启用 stator-temp-optimizer。请先发送：启用 stator-temp-optimizer Skill。`
- Before an authorized run, read the full `references/research-execution-spec.md`, inspect existing `Ablation/` progress and resume without overwriting experiments. Run no more than three new formal experiment versions per call.
- `退出迭代模式` or `停用 stator-temp-optimizer` sets this conversation to `INACTIVE`. Handle any running training safely and preserve recoverable checkpoints.
- Never persist the activation state. A new conversation or uncertain state is `INACTIVE`; durable progress belongs in `Ablation/experiment_state.json`.
- `/stator-temp-optimizer 迭代` is a one-call explicit request only; it does not activate later standalone shortcut messages. Quoting it is not authorization.
- Keep all research data and experiment artifacts local by default. Preserve the independent test set. GitHub synchronization requires separate explicit authorization.
- Do not restrict explicit invocation of other Skills.
