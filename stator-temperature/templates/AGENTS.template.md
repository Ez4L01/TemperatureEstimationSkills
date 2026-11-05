# Stator Temperature Project Instructions

Use these instructions only when this template is deliberately copied or merged into a research project's `AGENTS.md`. They do not apply globally. `stator-temp-prompts` and `stator-temp-optimizer` are independent Skills; these execution rules do not restrict explicit use of another Skill.

## Session gate for `stator-temp-optimizer`

- Every new agent conversation starts `INACTIVE`. Installing, discovering, loading, or reading the Skill does not activate it.
- Set the current conversation to `ACTIVE` only after the user clearly asks to enable the Skill in this conversation, for example `启用 stator-temp-optimizer Skill。`, Codex's `使用 $stator-temp-optimizer，启用本次会话的迭代模式。`, or the host's explicit `/stator-temp-optimizer 启用迭代模式` form.
- A mention, quotation, discussion, document, code comment, or example containing `stator-temp-optimizer` or `迭代` is not an enable or run request.
- Only when the current conversation is `ACTIVE` and has not been deactivated does a latest user message whose trimmed content is exactly `迭代` authorize this Skill. Otherwise, do not inspect or modify the research project, create experiment files, or train. Reply: `当前对话尚未启用 stator-temp-optimizer。请先发送：使用 $stator-temp-optimizer，启用本次会话的迭代模式。`
- On an authorized iteration, read the complete `references/research-execution-spec.md`, inspect `Ablation/` and resume from existing progress. Never replace an existing experiment. Run at most three new formal experiment versions in one call, including a baseline if needed.
- `退出迭代模式` or `停用 stator-temp-optimizer` returns this conversation to `INACTIVE`. Stop starting experiments; safely stop running work and preserve usable checkpoints and records where possible.
- Activation is session-only and must never be written to persistent project settings. A new conversation starts `INACTIVE`; if activation history is unclear, require re-enablement. Keep durable experiment progress separately in `Ablation/experiment_state.json`.
- An explicit host-native Skill invocation paired with a clear request to run one iteration (for example, `$stator-temp-optimizer 迭代` in Codex or `/stator-temp-optimizer 迭代` on a slash-command host) authorizes that call only. It does not activate later standalone `迭代` messages. A quoted or discussed invocation is not authorization.
- Keep research code, data, weights, checkpoints, logs, plots, and results local by default. Any GitHub synchronization requires separate explicit authorization. Never use test data for model selection or training.
- Do not restrict the user's direct, explicit invocation of other Skills.
