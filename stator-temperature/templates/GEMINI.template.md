# Stator Temperature Project Instructions

Use this template only when deliberately copied or merged into the research project's `GEMINI.md`. These are project instructions, not user-level settings. `stator-temp-prompts` and `stator-temp-optimizer` are independent Skills.

## Session gate for `stator-temp-optimizer`

- Start every Gemini CLI conversation `INACTIVE`. Installing, discovering, listing, loading, or reading the Skill does not activate iteration or start training.
- Activate only after the user clearly asks to enable it in the current conversation, for example `启用 stator-temp-optimizer Skill。`. If using a host-supported explicit Skill command, pair it with a clear enable request; do not assume an undocumented Gemini CLI slash command.
- A mention, quotation, document, or example containing the Skill name or `迭代` does not enable or execute it.
- Only while `ACTIVE`, a latest user message whose trimmed content is exactly `迭代` may run the optimizer. Otherwise do not inspect or modify the research project; reply: `当前对话尚未启用 stator-temp-optimizer。请先发送：启用 stator-temp-optimizer Skill。`
- Before running, read the complete `references/research-execution-spec.md` and inspect `Ablation/`; resume existing progress without overwriting it and add at most three new formal experiment versions per call.
- `退出迭代模式` or `停用 stator-temp-optimizer` resets the current conversation to `INACTIVE`. A new conversation or uncertain state is also `INACTIVE`.
- Keep activation in conversation context only. Store durable experiment progress in `Ablation/experiment_state.json`.
- A clear user request naming `stator-temp-optimizer` and asking to run one iteration authorizes that run only; it does not activate later standalone `迭代` messages.
- Keep research data and experiment artifacts local by default. Preserve the independent test set. GitHub synchronization requires separate explicit authorization.
- Do not restrict explicit use of other Skills.
