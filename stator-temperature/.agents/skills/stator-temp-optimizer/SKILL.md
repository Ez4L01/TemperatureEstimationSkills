---
name: stator-temp-optimizer
description: Optimize neural-network-based motor stator-temperature models through local training, validation, hardware acceleration, hyperparameter search, and ablation experiments. The standalone “迭代” shortcut requires explicit activation in the current agent conversation.
---

# Stator Temperature Optimizer

This execution skill is independent of the ordinary Markdown prompt library in `stator-temperature/prompts/`. It can analyze and optimize a neural-network project, run baseline and ablation experiments, and resume local work. Its complete research protocol is in [references/research-execution-spec.md](references/research-execution-spec.md). The instructions apply to any Agent Skills-compatible host; native invocation syntax differs by agent.

## Session activation gate

Keep a conversation-level authorization state with exactly two values: `INACTIVE` and `ACTIVE`. The default is `INACTIVE` for every new agent conversation.

- Installing, discovering, or loading this Skill does not activate it.
- Treat the state as `ACTIVE` only after the current user clearly issues an activation command in this conversation and no later deactivation has occurred. The host's Skill installation, discovery, or invocation syntax does not by itself activate the standalone shortcut.
- Accept these activation commands:
  - `启用 stator-temp-optimizer Skill。`
  - `使用 $stator-temp-optimizer，启用本次会话的迭代模式。` (Codex)
  - `$stator-temp-optimizer 启用迭代模式` (Codex)
  - `/stator-temp-optimizer 启用迭代模式` (hosts that support slash-based Skill invocation)
- A host-native Skill invocation without an explicit enable request only loads the Skill. Do not infer session activation or permission to train from loading alone.
- A mention, quotation, discussion, document, or code comment containing the Skill name or an activation phrase is not an activation command.
- The state belongs only to this conversation. Never store `ACTIVE` in a project file or infer it from installation or experiment records. A new conversation starts `INACTIVE`; if the current conversation's activation history is missing or uncertain, treat it as `INACTIVE` and ask the user to enable the Skill again.

When the user explicitly enables the Skill, read this file and the complete research specification, then check whether the open project is suitable and the specification is accessible. Mark this conversation `ACTIVE` and confirm that the standalone `迭代` command is available. Enabling the Skill is not permission to start training; do not begin an experiment during activation.

## Handling `迭代`

Interpret the shortcut only when the latest user message, after trimming leading and trailing whitespace, is exactly `迭代`.

- If the conversation is `INACTIVE`, do not inspect or modify the research project and do not run training. Reply: `当前对话尚未启用 stator-temp-optimizer。请先发送：使用 $stator-temp-optimizer，启用本次会话的迭代模式。`
- If the conversation is `ACTIVE`, read the research specification, inspect the current neural-network project and its `Ablation` records, then resume safely. If no baseline exists, begin with the baseline. Otherwise continue from saved experiment state and create new, uniquely numbered experiment versions; never replace existing results.
- Execute at most three new formal experiment versions per `迭代` call, including a baseline if it must be created. Respect any lower limit in the local project configuration.
- Save code, model artifacts, logs, plots, experiment records, and checkpoints locally. Do not upload research data or results to GitHub without separate explicit authorization.
- After the call, report what ran, the results, and the next candidate direction. Preserve progress so a later enabled conversation can resume.

The experiment state belongs in the research project at `Ablation/experiment_state.json`, not in this Skill repository. It may record the current experiment number, completed count, best model, recent results, checkpoint path, and next candidate directions. This file records experiment progress only; its presence never activates the Skill.

## Deactivation and explicit one-shot invocation

- `退出迭代模式` or `停用 stator-temp-optimizer` immediately changes this conversation to `INACTIVE`. Do not start another experiment. If training is underway, stop safely and preserve a usable checkpoint and records where possible.
- After deactivation, a standalone `迭代` is inert until the user explicitly enables the Skill again.
- An explicit host-native Skill invocation combined with a clear request to run one iteration authorizes that one iteration even if the conversation is `INACTIVE` (for example, `$stator-temp-optimizer 迭代` in Codex or `/stator-temp-optimizer 迭代` on a slash-command host). Treat it as one-shot execution; it does not activate later standalone `迭代` messages. A bare Skill invocation only loads instructions. A quoted or discussed copy of an invocation is not an execution request.
- These rules govern only this Skill. They do not restrict the user's direct invocation of another Skill.

## Research defaults

Use the full protocol in [references/research-execution-spec.md](references/research-execution-spec.md). Unless the local project configuration sets a lower or otherwise explicit value, use these defaults:

- Maximum 30 formal optimization experiment versions overall.
- Maximum 3 new formal experiment versions per `迭代` call.
- Hold out 10% of the original training set as a fixed validation set; keep the original test set independent.
- Initial Early Stopping patience: 15.
- Random seed: 42.
- Prefer CUDA when it is available and compatible.
- Reassess the search strategy after 8 consecutive formal experiments without material improvement.

Do not modify the independent test set, and keep all experiment artifacts local by default.
