# TemperatureEstimationSkills

本项目是面向温度估计与预测科研任务的 AI Agent Skills 与提示词资料仓库，旨在为神经网络开发、模型优化、科研实验和自动化研究流程提供可复用的指令与工作流。仓库按研究专题组织，可随着研究方向逐步扩展。

## 仓库内容

| 资源类型 | 当前内容 | 用途 |
| --- | --- | --- |
| Agent Skills | [stator-temp-optimizer](stator-temperature/.agents/skills/stator-temp-optimizer/SKILL.md) | 可安装并调用的定子温度估计科研执行型 Skill。 |
| 科研提示词资料库 | [stator-temperature/prompts/](stator-temperature/prompts/README.md) | 普通 Markdown 文档，用于保存、整理、查找和复制提示词；无需安装为 Skill。 |

当前定子温度专题仅包含 `stator-temp-optimizer` 这一项可安装 Skill。提示词资料库与执行型 Skill 相互独立；阅读或复制提示词不会自动执行其中的任务。

## 研究方向

目前收录电机定子温度估计（Stator Temperature Estimation）相关资源。后续可按实际内容增加其他温度估计研究专题。

## stator-temp-optimizer

该 Skill 面向基于神经网络的电机定子温度预测研究，主要覆盖：

- 神经网络项目分析与基线模型训练。
- CUDA 和计算硬件加速。
- 网络架构与超参数优化。
- 物理特征研究及科研文献分析。
- 消融实验与 RMSE、MeanRMSE、PooledRMSE、MaxAbs 评价。
- 逐工况预测曲线、误差曲线和结果分析。
- 本地 Ablation 版本记录、排行榜、Checkpoint 与断点恢复。
- 最终全量训练及原始独立测试集评价。

查看 [SKILL.md](stator-temperature/.agents/skills/stator-temp-optimizer/SKILL.md) 了解调用规则；完整流程见[科研执行规范](stator-temperature/.agents/skills/stator-temp-optimizer/references/research-execution-spec.md)。

## 快速安装

安装需要 Node.js 和 npm 提供的 `npx`。请在目标科研项目目录中执行以下命令，默认安装到当前项目；这不是全局安装。

```bash
# 查看仓库中可安装的 Skill
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --list

# 安装当前唯一的执行型 Skill
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer

# 也可以发现仓库并交互选择
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills
```

如需指定 Agent 或进行用户级安装，请参阅[跨 Agent 安装指南](docs/installation.md)。

## 支持的 AI Agent

以下路径与调用方式按 Skills CLI 和各平台文档整理。此前已完成 CLI 安装路径检查；宿主 Agent 内的原生加载与实际执行并未全部实测。

| Agent | 推荐项目安装路径 | 推荐调用方式 | 验证状态 |
| --- | --- | --- | --- |
| OpenAI Codex | `.agents/skills/` | `$stator-temp-optimizer`，随后明确启用 | CLI 目标路径已检查；Codex 原生运行未单独实测 |
| Claude Code | `.claude/skills/` | `/stator-temp-optimizer`，随后明确启用 | CLI 目标路径已检查；Claude Code 原生运行未单独实测 |
| Cursor | `.agents/skills/` | 使用 `/` 菜单选择 Skill，再明确启用 | CLI 目标路径已检查；Cursor 原生运行未单独实测 |
| Google Antigravity | `.agents/skills/` | `/stator-temp-optimizer`，随后明确启用 | CLI 目标路径已检查；Antigravity 原生运行未单独实测 |
| Gemini CLI | `.agents/skills/` | 在交互界面使用 `/stator-temp-optimizer`，并明确要求启用本次会话 | CLI 目标路径已检查；Gemini CLI 原生运行未单独实测 |
| DeepSeek Harness（DSH） | `.agents/skills/` 直接子目录 | 使用已启用的 Skill Catalog / `skill` 工具按名称加载 | 依据官方目录文档检查；DSH 原生运行未实测，官方资料未说明 `/stator-temp-optimizer` 斜杠命令 |

六个平台均使用同一份 Skill 源文件和科研执行规范。安装到对应目录不代表平台运行时已验证成功；各平台的前置组件和调用入口可能不同。详细说明见[安装指南](docs/installation.md)。

### DeepSeek Harness 安装

当前 Skills CLI 的目标列表没有 DSH 专用标识。可使用通用 `universal` 目标，将 Skill 安装到项目内的 `.agents/skills/`：

```bash
npx skills add https://github.com/Ez4L01/TemperatureEstimationSkills --skill stator-temp-optimizer --agent universal --copy --yes
```

DSH 需要启用本地 Skill filesystem provider 和相应的 Skill catalog/consumer；安装目录中 Skill 必须是 `.agents/skills/` 的直接子目录。DSH 原生发现与加载尚未在本环境实测。更多说明见[安装指南中的 DSH 部分](docs/installation.md#deepseek-harness-dsh)。

## Skill 使用方式

`stator-temp-optimizer` 的“迭代”快捷口令按当前对话单独激活：

1. 发送 `启用 stator-temp-optimizer Skill。`。Codex 也可发送 `使用 $stator-temp-optimizer，启用本次会话的迭代模式。`。启用时读取 Skill 并检查项目适用性，不会立即训练。
2. 确认当前对话已启用后，单独发送 `迭代`，开始或继续优化实验。
3. 发送 `退出迭代模式` 或 `停用 stator-temp-optimizer`，关闭当前对话的快捷执行模式。

安装或读取 Skill 不等于激活。每个新对话默认未激活，必须重新启用；退出后也必须重新启用。“迭代”只在当前对话明确激活后生效。实验进度记录在科研项目本地的 `Ablation/` 中，可供后续对话在重新启用后恢复。不同 Agent 对会话指令的支持方式不同，必要时使用平台提供的 Skill 显式调用入口；显式调用仍须明确表达启用或执行意图。

## 科研提示词资料库

[stator-temperature/prompts/](stator-temperature/prompts/README.md) 以 Markdown 保存提示词，并通过[提示词索引](stator-temperature/prompts/index.md)检索。可以直接在 GitHub 阅读，或让具有文件访问权限的 Agent 查找并展示正文。它是普通资料库，不属于可安装或自动执行的 Skill。

## 仓库目录

```text
TemperatureEstimationSkills/
├── README.md
├── LICENSE
├── docs/
│   └── installation.md
└── stator-temperature/
    ├── .agents/skills/
    │   └── stator-temp-optimizer/
    │       ├── SKILL.md
    │       └── references/
    │           └── research-execution-spec.md
    ├── prompts/
    │   ├── README.md
    │   └── index.md
    ├── templates/
    │   ├── AGENTS.template.md
    │   ├── ANTIGRAVITY-rule.template.md
    │   ├── CLAUDE.template.md
    │   ├── CURSOR.template.mdc
    │   ├── DSH-AGENTS.template.md
    │   ├── GEMINI.template.md
    │   └── README.md
    └── tests/
        ├── test_activation_policy.py
        └── test_repository_compatibility.py
```

## 数据保护与使用注意事项

- 模型训练默认在本地科研项目中执行。
- 原始训练集和独立测试集应保持隔离；优化实验结果默认保存在本地 `Ablation/`。
- 本仓库主要保存 Skill 定义、提示词和公开文档，不包含实际训练数据或模型产物。
- 安装 Skill 不会自动上传实验数据；向 GitHub 推送代码或实验文件需要用户另行明确授权。
- 会话级激活规则仅约束 Skill 的调用意图，不替代 Agent 自身的文件、终端和其他权限控制。

## 更新与许可证

在安装 Skill 的目标项目目录中运行 `npx skills update stator-temp-optimizer` 更新；使用 `npx skills remove stator-temp-optimizer` 移除项目级安装。已安装的旧版 `stator-temp-prompts` 不会因本仓库变更自动卸载，需在原项目中手动移除。

本仓库遵循 [LICENSE](LICENSE) 中的 MIT License。许可证条款以该文件为准。
