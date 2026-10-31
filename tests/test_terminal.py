import subprocess
from types import SimpleNamespace

import pytest

from ghostshell.terminal import Terminal, TerminalError, TerminalTimeout


def test_read_strips_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "  git status  ")
    assert Terminal().read("> ") == "git status"


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        ("", False),
        ("n", False),
        ("no", False),
        ("y", True),
        ("yes", True),
        ("YES", True),
    ],
)
def test_confirm(monkeypatch, answer, expected):
    monkeypatch.setattr("builtins.input", lambda prompt: answer)
    assert Terminal().confirm("Run?") is expected


def test_confirm_can_default_to_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "")
    assert Terminal().confirm("Run?", default=True) is True


def test_run_returns_the_runner_exit_code():
    terminal = Terminal(runner=lambda command, timeout: SimpleNamespace(returncode=7))
    assert terminal.run("Get-ChildItem") == 7


def test_missing_shell_is_reported():
    def runner(command, timeout):
        raise FileNotFoundError

    terminal = Terminal(runner=runner)
    with pytest.raises(TerminalError, match="Cannot start"):
        terminal.run("Get-ChildItem")


def test_command_timeout_is_reported():
    def runner(command, timeout):
        raise subprocess.TimeoutExpired(command, timeout)

    terminal = Terminal(runner=runner)
    with pytest.raises(TerminalTimeout, match="too long"):
        terminal.run("Get-ChildItem")


def test_default_runner_uses_shell_false(monkeypatch):
    captured = {}

    def fake_run(arguments, **kwargs):
        captured["arguments"] = arguments
        captured["kwargs"] = kwargs
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert Terminal().run("Get-ChildItem") == 0
    assert captured["arguments"][-1] == "Get-ChildItem"
    assert captured["kwargs"]["shell"] is False
    assert captured["kwargs"]["timeout"] == 120.0
