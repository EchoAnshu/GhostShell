"""Terminal output with optional color."""

from __future__ import annotations

import os
import sys
from typing import TextIO

RESET = "\x1b[0m"
CYAN = "36"
MAGENTA = "35"
YELLOW = "33"
RED = "31"
GREEN = "32"
DIM = "90"


class Console:
    """Small wrapper around a text stream."""

    def __init__(self, color: bool = True, stream: TextIO | None = None) -> None:
        self.stream = stream if stream is not None else sys.stdout
        self.color = color and self._stream_supports_color()

    def _stream_supports_color(self) -> bool:
        if os.environ.get("NO_COLOR"):
            return False
        isatty = getattr(self.stream, "isatty", None)
        return bool(isatty and isatty())

    def _paint(self, code: str, text: str) -> str:
        if not self.color:
            return text
        return f"\x1b[{code}m{text}{RESET}"

    def write(self, text: str = "", end: str = "\n") -> None:
        print(text, end=end, file=self.stream, flush=True)

    def banner(self) -> None:
        self.write(self._paint(CYAN, "GhostShell"))
        self.write(self._paint(DIM, "A haunted local terminal companion."))
        self.write(self._paint(DIM, "The ghost can be wrong. Review every explanation."))
        self.write(self._paint(DIM, "Type /help for commands. Type /exit to leave."))

    def section(self, label: str) -> None:
        self.write()
        self.write(self._paint(MAGENTA, f"[ {label} ]"))

    def hint(self, text: str) -> None:
        self.write(self._paint(DIM, text))

    def warning(self, text: str) -> None:
        self.write(self._paint(YELLOW, text))

    def error(self, text: str) -> None:
        self.write(self._paint(RED, text))

    def success(self, text: str) -> None:
        self.write(self._paint(GREEN, text))

    def help(self) -> None:
        self.section("GHOSTSHELL HELP")
        self.write("  explain <command>   Explain a command without running it")
        self.write("  /help               Show this help")
        self.write("  /check              Check Ollama and the selected model")
        self.write("  /exit               Leave GhostShell")
