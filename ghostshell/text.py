"""Clean model text before it reaches the terminal."""

from __future__ import annotations

import re

ANSI_PATTERN = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\)|[@-_])")
CONTROL_PATTERN = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
FENCE_PATTERN = re.compile(r"```[a-zA-Z0-9_+-]*[ \t]*\r?\n?|```")


def _clean_fragment(text: str) -> str:
    cleaned = ANSI_PATTERN.sub("", text)
    cleaned = FENCE_PATTERN.sub("", cleaned)
    cleaned = CONTROL_PATTERN.sub("", cleaned)
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"\n{3,}", "\n\n", cleaned)


def _shorten(text: str, max_chars: int) -> str:
    if max_chars <= 0:
        return ""
    if len(text) <= max_chars:
        return text
    limit = max(1, max_chars - 3)
    cut = text[:limit]
    space = cut.rfind(" ")
    if space >= limit // 2:
        cut = cut[:space]
    return cut.rstrip() + "..."


def sanitize(text: str, max_chars: int = 600) -> str:
    """Return printable, shortened text."""
    if not text:
        return ""
    return _shorten(_clean_fragment(text).strip(), max_chars)


class StreamSanitizer:
    """Clean streamed text while holding back split escape sequences."""

    def __init__(self, max_chars: int = 600) -> None:
        self.max_chars = max_chars
        self._buffer = ""
        self._emitted = 0
        self._stopped = False

    def _emit(self, text: str) -> str:
        if self._stopped or not text:
            return ""
        cleaned = _clean_fragment(text)
        remaining = self.max_chars - self._emitted
        if remaining <= 0:
            self._stopped = True
            return ""
        if len(cleaned) > remaining:
            cleaned = cleaned[:remaining]
            self._stopped = True
        self._emitted += len(cleaned)
        return cleaned

    def feed(self, chunk: str) -> str:
        """Clean one model chunk and return the printable part."""
        if self._stopped or not chunk:
            return ""
        self._buffer += chunk

        escape = self._buffer.rfind("\x1b")
        if escape != -1:
            safe = self._buffer[:escape]
            self._buffer = self._buffer[escape:]
        else:
            safe = self._buffer
            self._buffer = ""

        if safe.endswith("\r"):
            self._buffer = "\r" + self._buffer
            safe = safe[:-1]

        fence = safe.rfind("`")
        if fence != -1 and fence >= len(safe) - 3:
            self._buffer = safe[fence:] + self._buffer
            safe = safe[:fence]

        return self._emit(safe)

    def flush(self) -> str:
        """Return any held-back text and stop accepting input."""
        if self._stopped:
            self._buffer = ""
            return ""
        text = self._emit(self._buffer)
        self._buffer = ""
        self._stopped = True
        return text
