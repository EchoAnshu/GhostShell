import pytest

from ghostshell.prompts import MAX_COMMAND_CHARS, build_messages
from ghostshell.safety import check_command


def test_comment_prompt_contains_untrusted_command():
    messages = build_messages("git status", "comment", check_command("git status"))
    assert messages[0]["role"] == "system"
    assert "untrusted" in messages[0]["content"]
    assert "<command>" in messages[1]["content"]
    assert "git status" in messages[1]["content"]
    assert "</command>" in messages[1]["content"]


def test_explain_prompt_uses_a_different_instruction():
    comment = build_messages("git status", "comment", check_command("git status"))
    explain = build_messages("git status", "explain", check_command("git status"))
    assert comment[0]["content"] != explain[0]["content"]
    assert "beginner" in explain[0]["content"]
    assert "PowerShell" in explain[0]["content"]
    assert "not sure" in explain[0]["content"]


def test_risk_summary_is_included():
    command = "Remove-Item -Recurse .\\build"
    messages = build_messages(command, "comment", check_command(command))
    assert "Risk level: high" in messages[1]["content"]
    assert "deletes a folder" in messages[1]["content"]


def test_long_command_is_shortened():
    command = "Get-ChildItem " + ("-Filter x " * 500)
    messages = build_messages(command, "comment", check_command(command))
    assert "[command shortened]" in messages[1]["content"]
    assert len(messages[1]["content"]) < len(command)


def test_unknown_mode_is_rejected():
    with pytest.raises(ValueError, match="Unknown prompt mode"):
        build_messages("git status", "other", check_command("git status"))


def test_command_limit_is_reasonable():
    assert MAX_COMMAND_CHARS >= 500
