---
name: stator-temp-prompts
description: Save, organize, find, and display prompts used in neural-network-based motor stator temperature estimation research. Use when managing or retrieving those prompts; displaying a prompt does not run it.
---

# Stator Temperature Research Prompts

This skill is a prompt collection, not an automated research agent. Use it only to manage and present prompt text. Never execute a stored prompt just because it was requested or displayed.

## Use

- When asked to view the stator temperature research prompt directory, list the categories and the available prompt titles with a brief description of each.
- When asked to display or copy a specific prompt, read its linked Markdown file and return the complete text, including its replaceable variables. Do not shorten or paraphrase it.
- Showing, copying, or managing a prompt is separate from executing it. Do not start model training or other research work when the user only asks to view, copy, or manage a prompt.
- Execute a stored prompt as a research task specification only when the user explicitly asks you to carry it out.
- When given a new prompt to save, preserve its original meaning and key details, classify it under the closest category, save its complete body in Markdown, and register its title, purpose, replaceable variables, and link in [references/prompts.md](references/prompts.md). Do not overwrite existing prompts.
- The complete model optimization, hardware acceleration, and ablation prompt is [references/stator-temp-optimization.md](references/stator-temp-optimization.md). Read that file when the user asks to view or copy it.

## Prompt Index

Prompt categories and their entries are maintained in [references/prompts.md](references/prompts.md):

- 科研思路与研究方案
- 电机热物理机理分析
- 神经网络开发与代码调试
- 实验设计与结果分析
- 学术论文写作与润色
