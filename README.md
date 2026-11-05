# TemperatureEstimationSkills

Agent Skills for temperature-estimation research. Stator-temperature Skills are collected under `stator-temperature/.agents/skills/` and can be installed independently.

## Stator temperature estimation

- [stator-temp-prompts](stator-temperature/.agents/skills/stator-temp-prompts/SKILL.md) manages, classifies, finds, and displays research prompts. It does not execute them. Invoke `$stator-temp-prompts` to list or display a prompt.
- [stator-temp-optimizer](stator-temperature/.agents/skills/stator-temp-optimizer/SKILL.md) independently analyzes neural-network projects and performs model optimization and ablation experiments. Its complete research protocol is in [research-execution-spec.md](stator-temperature/.agents/skills/stator-temp-optimizer/references/research-execution-spec.md).

### Using the optimizer

1. Install the `stator-temp-optimizer` Skill from `stator-temperature/.agents/skills/stator-temp-optimizer/` into the target neural-network project.
2. In each Codex conversation where you want the shortcut, explicitly enable it by sending `使用 $stator-temp-optimizer，启用本次会话的迭代模式。` (or one of the other activation commands in its `SKILL.md`). Enabling only checks readiness; it does not start training.
3. Send `迭代` to run the next batch of optimization experiments. Send `迭代` again to resume from the saved experiment records. Each call adds at most 3 formal experiment versions.
4. Send `退出迭代模式` or `停用 stator-temp-optimizer` to disable the shortcut. Exiting does not delete experiment progress or artifacts.
5. A new Codex conversation starts inactive and must be explicitly enabled again. Experiment progress is kept separately at `Ablation/experiment_state.json` in the research project.

For a directly requested one-off run, `$stator-temp-optimizer 迭代` explicitly invokes one iteration without enabling later standalone `迭代` messages. Ordinary discussion or quotation of `迭代` never starts training.

`stator-temp-prompts` and `stator-temp-optimizer` are independent Skills: one manages prompt text; the other executes local research workflows. Research data, models, checkpoints, logs, and results stay local by default. Any GitHub synchronization requires separate explicit authorization.
