"""Static compatibility checks for the shared Agent Skills repository.

These checks inspect documentation and package structure only. They never
import a research project, create experiment artifacts, or run model training.
"""

from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit


REPO = Path(__file__).resolve().parents[2]
TOPIC = REPO / "stator-temperature"
SKILLS = TOPIC / ".agents" / "skills"
OPTIMIZER = SKILLS / "stator-temp-optimizer"
PROMPTS = TOPIC / "prompts"

try:
    import yaml
except ImportError:  # The repository has no Python dependencies.
    yaml = None


def frontmatter(text: str) -> dict[str, object]:
    """Parse YAML frontmatter when PyYAML is available; otherwise check keys."""
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", text, re.DOTALL)
    if not match:
        raise AssertionError("Missing YAML frontmatter")
    raw = match.group(1)
    if yaml is not None:
        value = yaml.safe_load(raw)
        if not isinstance(value, dict):
            raise AssertionError("Frontmatter must parse to a YAML mapping")
        return value

    result: dict[str, object] = {}
    for line in raw.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def local_markdown_targets(path: Path) -> list[Path]:
    """Return relative Markdown destinations in a Markdown file."""
    targets = []
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
        target = target.split(maxsplit=1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("#"):
            continue
        targets.append(path.parent / parsed.path)
    return targets


class RepositoryCompatibilityTests(unittest.TestCase):
    def test_skill_folders_match_frontmatter_names(self):
        expected = {"stator-temp-optimizer"}
        self.assertEqual({p.name for p in SKILLS.iterdir() if p.is_dir()}, expected)
        for name in expected:
            skill_file = SKILLS / name / "SKILL.md"
            self.assertTrue(skill_file.is_file())
            metadata = frontmatter(skill_file.read_text(encoding="utf-8"))
            self.assertEqual(metadata.get("name"), name)
            self.assertTrue(metadata.get("description"))

    def test_all_skill_reference_links_resolve(self):
        skill_file = OPTIMIZER / "SKILL.md"
        for target in local_markdown_targets(skill_file):
            self.assertTrue(target.is_file(), f"{skill_file}: missing {target}")

    def test_optimizer_is_independent_and_keeps_the_full_research_spec(self):
        optimizer_text = (OPTIMIZER / "SKILL.md").read_text(encoding="utf-8")
        spec_path = OPTIMIZER / "references" / "research-execution-spec.md"
        self.assertTrue(spec_path.is_file())
        self.assertNotIn("stator-temp-prompts", optimizer_text)
        spec = spec_path.read_text(encoding="utf-8")
        self.assertIn("## 20. Agent 自主执行总原则", spec)
        for required in ("10%", "Early Stopping", "CUDA", "MeanRMSE", "PooledRMSE", "MaxAbs", "Checkpoint"):
            self.assertIn(required, spec)
        self.assertIn("不得将测试集用于梯度训练", spec)
        self.assertIn("必须优先保存到项目本地的 `Ablation` 文件夹中", spec)
        index = PROMPTS / "index.md"
        self.assertTrue(index.is_file())
        self.assertIn("../.agents/skills/stator-temp-optimizer/references/research-execution-spec.md", index.read_text(encoding="utf-8"))
        self.assertEqual(len(list(REPO.rglob("research-execution-spec.md"))), 1)
        self.assertEqual(list(REPO.rglob("stator-temp-optimization.md")), [])

    def test_prompt_library_is_markdown_not_an_installable_skill(self):
        self.assertTrue((PROMPTS / "README.md").is_file())
        self.assertTrue((PROMPTS / "index.md").is_file())
        self.assertFalse((PROMPTS / "SKILL.md").exists())
        self.assertFalse((SKILLS / "stator-temp-prompts").exists())
        index = PROMPTS / "index.md"
        index_text = index.read_text(encoding="utf-8")
        for category in (
            "科研思路与研究方案",
            "电机热物理机理分析",
            "神经网络开发与代码调试",
            "实验设计与结果分析",
            "学术论文写作与润色",
        ):
            self.assertIn(category, index_text)
        for target in local_markdown_targets(index):
            self.assertTrue(target.is_file(), f"{index}: missing {target}")
        readme = PROMPTS / "README.md"
        for target in local_markdown_targets(readme):
            self.assertTrue(target.is_file(), f"{readme}: missing {target}")

    def test_sources_are_not_duplicated_at_repository_root(self):
        skill_files = list(REPO.rglob("SKILL.md"))
        self.assertEqual({path.parent.name for path in skill_files}, {"stator-temp-optimizer"})
        self.assertEqual(len(skill_files), 1)

    def test_project_templates_exist_and_keep_inactive_default(self):
        templates = TOPIC / "templates"
        expected = {
            "AGENTS.template.md",
            "DSH-AGENTS.template.md",
            "CLAUDE.template.md",
            "CURSOR.template.mdc",
            "GEMINI.template.md",
            "ANTIGRAVITY-rule.template.md",
        }
        self.assertTrue(expected.issubset({path.name for path in templates.iterdir()}))
        for name in expected:
            text = (templates / name).read_text(encoding="utf-8")
            self.assertIn("INACTIVE", text, name)
            self.assertIn("Ablation/experiment_state.json", text, name)
            self.assertIn("GitHub synchronization requires separate explicit authorization", text, name)
            self.assertNotIn("stator-temp-prompts", text, name)
        cursor = frontmatter((templates / "CURSOR.template.mdc").read_text(encoding="utf-8"))
        anti = frontmatter((templates / "ANTIGRAVITY-rule.template.md").read_text(encoding="utf-8"))
        dsh = (templates / "DSH-AGENTS.template.md").read_text(encoding="utf-8")
        gemini = (templates / "GEMINI.template.md").read_text(encoding="utf-8")
        self.assertIs(cursor.get("alwaysApply"), True)
        self.assertEqual(anti.get("trigger"), "always_on")
        self.assertIn("Skill catalog/consumer", dsh)
        self.assertNotIn("explicit DSH `/stator-temp-optimizer` invocation", dsh)
        self.assertIn("/stator-temp-optimizer 启用迭代模式", gemini)
        self.assertNotIn("do not assume an undocumented Gemini CLI slash command", gemini)

    def test_readme_and_install_guide_have_valid_relative_links(self):
        documents = sorted({*REPO.rglob("*.md"), *REPO.rglob("*.mdc")})
        self.assertTrue(documents)
        for path in documents:
            for target in local_markdown_targets(path):
                self.assertTrue(target.is_file(), f"{path}: missing {target}")
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        guide = (REPO / "docs" / "installation.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/Ez4L01/TemperatureEstimationSkills", readme)
        self.assertIn("--skill stator-temp-optimizer", readme)
        self.assertNotIn("--skill stator-temp-prompts", readme + guide)
        self.assertIn("stator-temperature/prompts/index.md", readme)
        self.assertIn("npx skills remove stator-temp-prompts", readme + guide)
        self.assertIn("--agent universal", guide)
        self.assertIn("deepseek-harness", guide.lower())
        self.assertNotIn("Ez4L01/StatorTempSkills", readme + guide)

    def test_homepage_is_chinese_and_documents_the_current_resources(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        self.assertTrue(readme.startswith("# TemperatureEstimationSkills\n\n本项目是"))
        for heading in (
            "## 仓库内容",
            "## 研究方向",
            "## stator-temp-optimizer",
            "## 快速安装",
            "## 支持的 AI Agent",
            "## Skill 使用方式",
            "## 科研提示词资料库",
            "## 仓库目录",
            "## 数据保护与使用注意事项",
            "## 更新与许可证",
        ):
            self.assertIn(heading, readme)
        for agent in (
            "OpenAI Codex",
            "Claude Code",
            "Cursor",
            "Google Antigravity",
            "Gemini CLI",
            "DeepSeek Harness（DSH）",
        ):
            self.assertIn(agent, readme)
        self.assertIn("stator-temperature/prompts/index.md", readme)
        self.assertIn("--skill stator-temp-optimizer", readme)
        self.assertIn("在交互界面使用 `/stator-temp-optimizer`", readme)
        self.assertNotIn("--skill stator-temp-prompts", readme)
        self.assertIn("MIT License", readme)

    def test_install_guide_is_chinese_and_distinguishes_runtime_validation(self):
        guide = (REPO / "docs" / "installation.md").read_text(encoding="utf-8")
        self.assertTrue(guide.startswith("# 安装与 Agent 兼容说明"))
        for phrase in (
            "DeepSeek Harness（DSH）",
            "OpenAI Codex",
            "Claude Code",
            "Google Antigravity",
            "Gemini CLI",
            "未实测",
            "本地仓库首页发现",
            "修改后 GitHub 仓库首页 URL",
            "--agent universal",
            "`/skills enable <name>`",
            "stator-temperature/prompts/index.md",
        ):
            self.assertIn(phrase, guide)
        self.assertNotIn("--skill stator-temp-prompts", guide)
        self.assertIn("官方资料未说明 `/stator-temp-optimizer` 斜杠命令", guide)
        self.assertNotIn("Ez4L01/StatorTempSkills", guide)

    def test_documentation_uses_current_repo_install_commands_and_only_one_skill(self):
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        guide = (REPO / "docs" / "installation.md").read_text(encoding="utf-8")
        for text in (readme, guide):
            self.assertIn("https://github.com/Ez4L01/TemperatureEstimationSkills", text)
            self.assertIn("stator-temp-optimizer", text)
            self.assertNotIn("--skill stator-temp-prompts", text)
        self.assertIn("stator-temp-prompts", guide)  # Manual cleanup for pre-existing installs.
        self.assertEqual({p.name for p in SKILLS.iterdir() if p.is_dir()}, {"stator-temp-optimizer"})


if __name__ == "__main__":
    unittest.main()
