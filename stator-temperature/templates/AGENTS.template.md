# Stator Temperature Project Instructions

These instructions apply only when this template is deliberately installed in a stator-temperature research project. They do not change user-level or global instructions. They do not restrict direct, explicit invocation of other Skills.

## `stator-temp-optimizer` conversation gate

- The default conversation state is `INACTIVE`. Installing, discovering, or loading `stator-temp-optimizer` does not activate it.
- Set the state to `ACTIVE` only after the user explicitly enables the Skill in the current Codex conversation with one of these commands:
  - `使用 $stator-temp-optimizer，启用本次会话的迭代模式。`
  - `启用 stator-temp-optimizer Skill。`
  - `$stator-temp-optimizer 启用迭代模式`
- Determine activation only from explicit user intent in the current conversation. A Skill name or `迭代` appearing in discussion, quoted text, documents, or code comments does not activate or execute it.
- A new Codex conversation starts `INACTIVE` and must be enabled again. After `退出迭代模式` or `停用 stator-temp-optimizer`, return to `INACTIVE` and require explicit re-enablement. If the state cannot be reliably confirmed, fail closed as `INACTIVE`.
- Only when the current conversation is `ACTIVE` and has not been deactivated does a user message consisting exactly of `迭代` after trimming surrounding whitespace authorize the optimizer workflow. Otherwise reply: `当前对话尚未启用 stator-temp-optimizer。请先发送：使用 $stator-temp-optimizer，启用本次会话的迭代模式。` Do not start training, inspect or modify project files, or create experiment artifacts in response to that inactive shortcut.
- The explicit user request `$stator-temp-optimizer 迭代` is a separate one-shot execution authorization, even while `INACTIVE`; it does not activate the conversation for later shortcut messages. Quoting or discussing that command is not authorization.
- Enabling the Skill only checks that its execution specification is available and that the open project is suitable. It does not start training.
- On an authorized iteration, read the full execution specification, inspect local experiment progress, and resume without replacing existing experiments. Limit each call to at most 3 new formal experiment versions, including a baseline if one is needed.
- Keep conversation activation separate from durable experiment progress. Store project progress in `Ablation/experiment_state.json`; never use that file as evidence of activation. A new conversation must be explicitly enabled before continuing with the standalone `迭代` shortcut.
- Preserve independent test data and keep training data, weights, checkpoints, logs, and experiment results local. GitHub synchronization requires separate explicit authorization.

## Other Skills

These activation rules apply only to `stator-temp-optimizer`. Handle a user's direct explicit invocation of another Skill under that Skill's own instructions.
