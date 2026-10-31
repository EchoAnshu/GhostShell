"""Input, confirmation, and command execution."""

from __future__ import annotations

import subprocess
from collections.abc import Callable

DEFAULT_COMMAND_TIMEOUT = 120.0


class TerminalError(RuntimeError):
    """Raised when the shell cannot run a command."""


class TerminalTimeout(TerminalError):
    """Raised when a command runs too long."""


Runner = Callable[[str, float], subprocess.CompletedProcess[str]]


class Terminal:
    """Interactive terminal boundary."""

    def __init__(self, shell: str = "powershell.exe", runner: Runner | None = None) -> None:
        self.shell = shell
        self._runner = runner if runner is not None else self._run_subprocess

    def read(self, prompt: str) -> str:
        return input(prompt).strip()

    def confirm(self, question: str, default: bool = False) -> bool:
        suffix = "[Y/n]" if default else "[y/N]"
        answer = input(f"{question} {suffix} ").strip().lower()
        if not answer:
            return default
        return answer in {"y", "yes"}

    def run(self, command: str, timeout: float = DEFAULT_COMMAND_TIMEOUT) -> int:
        try:
            completed = self._runner(command, timeout)
        except FileNotFoundError as exc:
            raise TerminalError(f"Cannot start {self.shell}. Is PowerShell installed?") from exc
        except subprocess.TimeoutExpired as exc:
            raise TerminalTimeout("The command took too long and was stopped.") from exc
        except OSError as exc:
            raise TerminalError(f"Cannot run the command: {exc}") from exc
        return completed.returncode

    def _run_subprocess(self, command: str, timeout: float) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [self.shell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
            timeout=timeout,
            shell=False,
            check=False,
        )
