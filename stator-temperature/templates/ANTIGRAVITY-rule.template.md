---
trigger: always_on
description: Keep stator-temp-optimizer iteration inactive until the user explicitly enables it in this conversation.
---

# Stator Temperature Project Instructions

- Start each Antigravity conversation `INACTIVE`. Finding or loading a Skill does not activate its shortcut or start training.
- Activate only after a clear user request in the current conversation, such as `启用 stator-temp-optimizer Skill。` or `/stator-temp-optimizer 启用迭代模式`.
- Mentions, quotations, documents, and examples do not enable or execute the Skill.
- Only while `ACTIVE`, a latest user message whose trimmed content is exactly `迭代` may run the optimizer. Otherwise do not inspect or modify the research project; reply: `当前对话尚未启用 stator-temp-optimizer。请先发送：启用 stator-temp-optimizer Skill。`
- Before an authorized run, read the complete `references/research-execution-spec.md` and inspect `Ablation/`; resume without overwriting prior experiments and add at most three new formal experiment versions per call.
- `退出迭代模式` or `停用 stator-temp-optimizer` resets this conversation to `INACTIVE`. New conversations and uncertain state are `INACTIVE` too.
- Keep activation in conversation context only; store durable progress in `Ablation/experiment_state.json`.
- `/stator-temp-optimizer 迭代` authorizes a single call only. It does not activate later standalone shortcut messages.
- Keep research data and experiment artifacts local by default. Preserve the independent test set. GitHub synchronization requires separate explicit authorization.
- This rule does not restrict explicit invocation of other Skills.
