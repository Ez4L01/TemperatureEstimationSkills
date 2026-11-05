"""No-training checks for the stator-temp-optimizer conversation gate.

The Skill is natural-language policy, so this file checks its written contract
and simulates the specified state transitions. It does not inspect a research
project or run model code.
"""

from dataclasses import dataclass
from pathlib import Path
import unittest


REPO = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO / "stator-temperature" / ".agents" / "skills"
OPTIMIZER_DIR = SKILL_DIR / "stator-temp-optimizer"
PROMPTS_DIR = REPO / "stator-temperature" / "prompts"
SKILL = (OPTIMIZER_DIR / "SKILL.md").read_text(encoding="utf-8")
AGENTS_TEMPLATE = (REPO / "stator-temperature" / "templates" / "AGENTS.template.md").read_text(encoding="utf-8")
SPEC = (OPTIMIZER_DIR / "references" / "research-execution-spec.md").read_text(encoding="utf-8")

ENABLE_COMMANDS = {
    "使用 $stator-temp-optimizer，启用本次会话的迭代模式。",
    "启用 stator-temp-optimizer Skill。",
    "$stator-temp-optimizer 启用迭代模式",
}
EXIT_COMMANDS = {"退出迭代模式", "停用 stator-temp-optimizer"}
ONE_SHOT = "$stator-temp-optimizer 迭代"


@dataclass
class SessionGate:
    """Small simulator for the documented session-only authorization rules."""

    active: bool | None = False
    completed_versions: tuple[str, ...] = ()

    def handle(self, message: str) -> str:
        command = message.strip()
        if command in EXIT_COMMANDS:
            self.active = False
            return "deactivated"
        if command in ENABLE_COMMANDS:
            self.active = True
            return "enabled_without_training"
        if command == ONE_SHOT:
            return "execute_one_iteration"
        if command == "迭代":
            if self.active is True:
                return "resume_from_experiment_state"
            return "refuse_and_request_activation"
        return "no_optimizer_execution"


class ActivationPolicyTests(unittest.TestCase):
    def test_contract_and_single_authoritative_spec_are_present(self):
        self.assertIn("name: stator-temp-optimizer", SKILL)
        self.assertNotIn("name: stator-temp-prompts", SKILL)
        self.assertIn("INACTIVE", SKILL)
        self.assertIn("ACTIVE", SKILL)
        self.assertIn("Ablation/experiment_state.json", SKILL)
        self.assertIn("Maximum 3 new formal experiment versions", SKILL)
        self.assertIn("direct, explicit invocation of other Skills", AGENTS_TEMPLATE)
        self.assertIn("never replace existing results", SKILL)
        for command in ENABLE_COMMANDS:
            self.assertIn(command, SKILL)
        self.assertIn("启用 stator-temp-optimizer Skill。", AGENTS_TEMPLATE)
        self.assertIn("Codex's", AGENTS_TEMPLATE)
        for term in ("10%", "Early Stopping", "CUDA", "MeanRMSE", "MaxAbs", "PooledRMSE"):
            self.assertIn(term, SPEC)
        self.assertIn("## 20. Agent 自主执行总原则", SPEC)
        self.assertIn("不得将测试集用于梯度训练", SPEC)
        self.assertIn("必须优先保存到项目本地的 `Ablation` 文件夹中", SPEC)
        self.assertTrue((PROMPTS_DIR / "index.md").is_file())
        self.assertIn("research-execution-spec.md", (PROMPTS_DIR / "index.md").read_text(encoding="utf-8"))
        self.assertFalse((SKILL_DIR / "stator-temp-prompts").exists())

    def test_01_new_conversation_starts_inactive(self):
        gate = SessionGate()
        self.assertEqual(gate.handle("迭代"), "refuse_and_request_activation")

    def test_02_installation_does_not_activate(self):
        installed_skill = True
        gate = SessionGate()
        self.assertTrue(installed_skill)
        self.assertEqual(gate.handle("迭代"), "refuse_and_request_activation")

    def test_03_activation_only_changes_session_state(self):
        for command in ENABLE_COMMANDS:
            with self.subTest(command=command):
                gate = SessionGate()
                self.assertEqual(gate.handle(command), "enabled_without_training")
                self.assertIs(gate.active, True)

    def test_04_active_standalone_iteration_is_allowed(self):
        gate = SessionGate()
        gate.handle("启用 stator-temp-optimizer Skill。")
        self.assertEqual(gate.handle("迭代"), "resume_from_experiment_state")

    def test_05_repeated_iteration_preserves_existing_versions(self):
        gate = SessionGate(active=True, completed_versions=("001_Baseline", "002_LearningRate"))
        before = gate.completed_versions
        self.assertEqual(gate.handle("迭代"), "resume_from_experiment_state")
        self.assertEqual(gate.completed_versions, before)

    def test_06_exit_requires_reactivation(self):
        gate = SessionGate(active=True)
        self.assertEqual(gate.handle("退出迭代模式"), "deactivated")
        self.assertEqual(gate.handle("迭代"), "refuse_and_request_activation")

    def test_07_new_conversation_does_not_inherit_activation(self):
        old = SessionGate(active=True)
        self.assertIs(old.active, True)
        new = SessionGate()
        self.assertEqual(new.handle("迭代"), "refuse_and_request_activation")

    def test_08_explicit_one_shot_invocation_is_allowed(self):
        gate = SessionGate()
        self.assertEqual(gate.handle(ONE_SHOT), "execute_one_iteration")
        self.assertIs(gate.active, False)

    def test_09_discussion_and_quoted_mentions_do_not_execute(self):
        gate = SessionGate()
        for message in (
            "我们讨论一下迭代策略。",
            "Skill 名称是 stator-temp-optimizer。",
            "引用：启用 stator-temp-optimizer Skill。",
            f"请解释命令 {ONE_SHOT} 的含义。",
        ):
            self.assertEqual(gate.handle(message), "no_optimizer_execution")

    def test_10_unknown_state_fails_closed(self):
        gate = SessionGate(active=None)
        self.assertEqual(gate.handle("迭代"), "refuse_and_request_activation")


if __name__ == "__main__":
    unittest.main()
