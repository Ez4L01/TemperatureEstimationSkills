# TemperatureEstimationSkills

An extensible collection of Agent Skills for temperature-estimation research. The repository currently includes a stator-temperature topic; each Skill has one maintained source and can be installed separately from this repository URL:

<https://github.com/Ez4L01/TemperatureEstimationSkills>

## Research topics and Skills

| Topic | Skill | Purpose |
| --- | --- | --- |
| Stator temperature estimation | [stator-temp-prompts](stator-temperature/.agents/skills/stator-temp-prompts/SKILL.md) | Save, classify, search, and display research prompts. Displaying a prompt does not execute it. |
| Stator temperature estimation | [stator-temp-optimizer](stator-temperature/.agents/skills/stator-temp-optimizer/SKILL.md) | Analyze neural-network projects and perform local model optimization, hardware acceleration, and ablation experiments after an explicit request. Full protocol: [research-execution-spec.md](stator-temperature/.agents/skills/stator-temp-optimizer/references/research-execution-spec.md). |

Skills are independent. Installing or viewing either Skill does not start model training. The optimizer's complete research protocol is shared across supported Agents.

## Install from the repository home URL

The current [Skills CLI](https://github.com/vercel-labs/skills) can discover Skills in this research-topic layout from the repository URL. Run these commands in the target research project:

```bash
# List all available Skills
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --list

# Install one Skill by name
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-prompts
```

To choose the Agent target explicitly, add `--agent` with the supported CLI ID, for example `--agent claude-code`, `--agent codex`, `--agent cursor`, `--agent antigravity`, or `--agent gemini-cli`. Add `--copy --yes` for a non-interactive copied install. Without `--agent`, the CLI uses its current Agent detection and install defaults. Project install is the default; use `--global` for a user-level install. Details and exact platform notes are in [docs/installation.md](docs/installation.md).

### DeepSeek Harness

The Skills CLI does not currently list a DeepSeek Harness-specific `--agent` target. Use its supported `universal` target, which installs a project Skill directly into `.agents/skills/<skill-name>/`:

```bash
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer --agent universal --copy --yes
```

DeepSeek Harness's filesystem Skill provider scans that direct-child project directory. If the DSH runtime has its Skill filesystem provider and Skill catalog consumer enabled, the Skill can be listed and explicitly loaded as `/stator-temp-optimizer`. Loading it does not start training. See [the DSH installation notes](docs/installation.md#deepseek-harness-dsh).

## Use the Skills

### `stator-temp-prompts`

Invoke `$stator-temp-prompts` in Codex, or use the platform's explicit Skill invocation. Ask to view the prompt directory or display a named prompt. The Skill returns the index or full Markdown text; it does not execute the stored prompt unless you separately ask it to do so.

### `stator-temp-optimizer`

1. Explicitly enable it in the current conversation with `启用 stator-temp-optimizer Skill。` (Codex also accepts `使用 $stator-temp-optimizer，启用本次会话的迭代模式。`; use a platform's documented explicit Skill invocation where appropriate).
2. Enabling reads the Skill and checks project readiness; it does not begin training.
3. After activation, send exactly `迭代` to start or resume up to three formal experiment versions. Existing local experiment records are preserved.
4. Send `退出迭代模式` or `停用 stator-temp-optimizer` to deactivate the shortcut.
5. Every new Agent conversation starts inactive and needs fresh activation. Exiting does not delete experiment progress.

For a single explicitly requested run, use the host's direct Skill invocation together with a clear request to run one iteration. This authorizes that run only; it does not activate later standalone `迭代` messages. A quoted command or ordinary discussion is not authorization.

Training data, model weights, checkpoints, logs, plots, and experiment results are saved locally by default. A Skill install or update is separate from experimental data handling. GitHub synchronization requires separate explicit authorization.

## Update or remove an installed Skill

```bash
# Update all installed Skills, or update one by name
npx skills update
npx skills update stator-temp-optimizer

# List installed Skills
npx skills list

# Remove one Skill
npx skills remove stator-temp-optimizer
```

## Repository layout

```text
TemperatureEstimationSkills/
├── README.md
├── docs/installation.md
└── stator-temperature/
    ├── .agents/skills/
    │   ├── stator-temp-prompts/
    │   └── stator-temp-optimizer/
    ├── templates/
    └── tests/
```

The Skills CLI was tested from the repository home URL and found both Skills. The domain-organized source layout remains unchanged because discovery and install by name work. See [compatibility notes and test coverage](docs/installation.md#compatibility-and-test-results).
