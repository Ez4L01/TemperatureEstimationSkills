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
PROMPTS = SKILLS / "stator-temp-prompts"

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
        expected = {"stator-temp-prompts", "stator-temp-optimizer"}
        self.assertEqual({p.name for p in SKILLS.iterdir() if p.is_dir()}, expected)
        for name in expected:
            skill_file = SKILLS / name / "SKILL.md"
            self.assertTrue(skill_file.is_file())
            metadata = frontmatter(skill_file.read_text(encoding="utf-8"))
            self.assertEqual(metadata.get("name"), name)
            self.assertTrue(metadata.get("description"))

    def test_all_skill_reference_links_resolve(self):
        for skill_file in SKILLS.glob("*/SKILL.md"):
            for target in local_markdown_targets(skill_file):
                self.assertTrue(target.is_file(), f"{skill_file}: missing {target}")

    def test_optimizer_is_independent_and_keeps_the_full_research_spec(self):
        optimizer_text = (OPTIMIZER / "SKILL.md").read_text(encoding="utf-8")
        spec_path = OPTIMIZER / "references" / "research-execution-spec.md"
        prompt_spec_path = PROMPTS / "references" / "stator-temp-optimization.md"
        self.assertTrue(spec_path.is_file())
        self.assertEqual(spec_path.read_bytes(), prompt_spec_path.read_bytes())
        self.assertNotIn("stator-temp-prompts must be installed", optimizer_text)
        spec = spec_path.read_text(encoding="utf-8")
        self.assertIn("## 20. Agent 自主执行总原则", spec)
        for required in ("10%", "Early Stopping", "CUDA", "MeanRMSE", "PooledRMSE", "MaxAbs", "Checkpoint"):
            self.assertIn(required, spec)

    def test_sources_are_not_duplicated_at_repository_root(self):
        skill_files = list(REPO.rglob("SKILL.md"))
        self.assertEqual({path.parent.name for path in skill_files}, {"stator-temp-prompts", "stator-temp-optimizer"})
        self.assertEqual(len(skill_files), 2)

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
        cursor = frontmatter((templates / "CURSOR.template.mdc").read_text(encoding="utf-8"))
        anti = frontmatter((templates / "ANTIGRAVITY-rule.template.md").read_text(encoding="utf-8"))
        self.assertIs(cursor.get("alwaysApply"), True)
        self.assertEqual(anti.get("trigger"), "always_on")

    def test_readme_and_install_guide_have_valid_relative_links(self):
        for path in (REPO / "README.md", REPO / "docs" / "installation.md", TOPIC / "templates" / "README.md"):
            self.assertTrue(path.is_file())
            for target in local_markdown_targets(path):
                self.assertTrue(target.is_file(), f"{path}: missing {target}")
        readme = (REPO / "README.md").read_text(encoding="utf-8")
        guide = (REPO / "docs" / "installation.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/Ez4L01/TemperatureEstimationSkills", readme)
        self.assertIn("--skill stator-temp-optimizer", readme)
        self.assertIn("--skill stator-temp-prompts", readme)
        self.assertIn("--agent universal", guide)
        self.assertIn("deepseek-harness", guide.lower())
        self.assertNotIn("Ez4L01/StatorTempSkills", readme + guide)


if __name__ == "__main__":
    unittest.main()
