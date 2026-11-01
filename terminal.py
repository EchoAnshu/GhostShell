"""Terminal interaction layer: display, safety checks, confirmation, execution.

The AI never decides anything here. Only the user's exact command may be
executed, only after an explicit confirmation (and a typed confirmation
for flagged commands). Model output is never passed to a shell.
"""

import subprocess
import sys
import time


# --- ANSI styling -----------------------------------------------------------

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
DIM = "\033[2m"
BOLD = "\033[1m"


def style(text: str, *codes: str) -> str:
    return "".join(codes) + text + RESET


def enable_ansi() -> None:
    """Enable virtual terminal processing on Windows consoles."""
    if sys.platform != "win32":
        return
    try:
        import ctypes

        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        mode = ctypes.c_uint32()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(
                handle, mode.value | 0x0004
            )
    except Exception:
        pass


HEADER_WHISPER = style("[ THE GHOST WHISPERS ]", CYAN, BOLD)
HEADER_ARCHIVIST = style("[ THE ARCHIVIST SPEAKS ]", MAGENTA, BOLD)
HEADER_WARNING = style("[ WARNING: RESTLESS SPIRIT ]", RED, BOLD)


HAUNTED_BANNER = """
    .-. _______ .-.
   ( ( )  GHOSTSHELL ( ) )
    '-/  _____  \\-'
      / |  o o|  \\
      \\ |  \\_/|  /
      {/|   | |}
       '-|_|_|-'
 Something is watching your terminal.
"""


if sys.platform == "win32":
    import ctypes

    class _COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class _SMALL_RECT(ctypes.Structure):
        _fields_ = [
            ("Left", ctypes.c_short),
            ("Top", ctypes.c_short),
            ("Right", ctypes.c_short),
            ("Bottom", ctypes.c_short),
        ]

    class _CONSOLE_SCREEN_BUFFER_INFOEX(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.c_ulong),
            ("dwSize", _COORD),
            ("dwCursorPosition", _COORD),
            ("wAttributes", ctypes.c_ushort),
            ("srWindow", _SMALL_RECT),
            ("dwMaximumWindowSize", _COORD),
            ("wPopupAttributes", ctypes.c_ushort),
            ("bFullscreenSupported", ctypes.c_bool),
            ("ColorTable", ctypes.c_uint32 * 16),
        ]


# COLORREF layout is 0x00BBGGRR.
_HAUNT_BACKGROUND = 0x280A1F  # deep haunt purple, RGB(31,10,40)
_HAUNT_TEXT = 0x8BD63D        # ghost green, RGB(61,214,139)
_HAUNT_RED = 0x1212C8         # blood red, RGB(200,18,18)

_SAVED_CONSOLE = None
_HAUNT_APPLIED = False


def _apply_windows_palette() -> bool:
    global _SAVED_CONSOLE, _HAUNT_APPLIED
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        info = _CONSOLE_SCREEN_BUFFER_INFOEX()
        info.cbSize = ctypes.sizeof(info)
        if not kernel32.GetConsoleScreenBufferInfoEx(handle, ctypes.byref(info)):
            return False
        _SAVED_CONSOLE = (info.ColorTable[0], info.ColorTable[7], info.ColorTable[1])
        info.ColorTable[0] = _HAUNT_BACKGROUND
        info.ColorTable[7] = _HAUNT_TEXT
        info.ColorTable[1] = _HAUNT_RED
        if not kernel32.SetConsoleScreenBufferInfoEx(handle, ctypes.byref(info)):
            return False
        _HAUNT_APPLIED = True
        return True
    except Exception:
        return False


def _restore_windows_palette() -> None:
    global _SAVED_CONSOLE, _HAUNT_APPLIED
    if not _HAUNT_APPLIED or _SAVED_CONSOLE is None:
        return
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)
        info = _CONSOLE_SCREEN_BUFFER_INFOEX()
        info.cbSize = ctypes.sizeof(info)
        if not kernel32.GetConsoleScreenBufferInfoEx(handle, ctypes.byref(info)):
            return
        info.ColorTable[0], info.ColorTable[7], info.ColorTable[1] = _SAVED_CONSOLE
        kernel32.SetConsoleScreenBufferInfoEx(handle, ctypes.byref(info))
    except Exception:
        pass
    finally:
        _SAVED_CONSOLE = None
        _HAUNT_APPLIED = False


def prompt_str() -> str:
    skull = style("\u2620", MAGENTA, BOLD)
    mark = style(">", CYAN, BOLD)
    return skull + " " + mark + " "


def _fade_in_banner() -> None:
    for line in HAUNTED_BANNER.splitlines():
        print(style(line, CYAN, BOLD))
        time.sleep(0.04)


def enter_haunted_mode() -> None:
    """Recolor the whole console to the Halloween palette and repaint it."""
    if sys.platform == "win32":
        _apply_windows_palette()
    else:
        # Non-Windows fallback: OSC palette for terminals that honour it.
        print("\033]11;#1f0a28\007\033]10;#3dd68b\007", end="")
    print("\033[2J\033[H", end="")
    _fade_in_banner()


def leave_haunted_mode() -> None:
    """Hand the console its own colors back."""
    if sys.platform == "win32":
        _restore_windows_palette()
    else:
        print("\033]111\007\033]110\007", end="")


# --- Deterministic risk checks ----------------------------------------------

RISK_PATTERNS = [
    (r"\brm\s+-[a-zA-Z]*[rR][a-zA-Z]*\b", "recursive file deletion"),
    (r"\brm\s+--recursive\b", "recursive file deletion"),
    (r"(?i)\bdel\b\s+/[sq]", "recursive file deletion"),
    (r"(?i)\brd\b\s+/s\b", "recursive folder deletion"),
    (r"(?i)\brmdir\b\s+/s\b", "recursive folder deletion"),
    (r"(?i)\bremove-item\b[^|\n;]*-recurse", "recursive file deletion"),
    (r"(?i)\bclear-content\b[^\n]*", "file content wipe"),
    (r"(?i)\bformat\b\s+[a-zA-Z]:", "drive formatting"),
    (r"(?i)\bmkfs\b[.\w]*", "filesystem formatting"),
    (r"\bdd\b\s+if=", "raw disk write"),
    (r"(?i)\b(shutdown|restart-computer|stop-computer)\b", "system shutdown or restart"),
    (r"(?i)\bsudo\b", "elevated privileges"),
    (r"(?i)\bchmod\b[^|\n;]*-R", "recursive permission change"),
    (r"(?i)\b(reg\s+delete|remove-itemprop)\b", "registry deletion"),
    (r"(?i)\bset-executionpolicy\b", "PowerShell execution policy change"),
    (r"(?i)\b(curl|wget)\b[^|\n]*\|\s*(sudo\s+)?(ba|z|da|fi)?sh\b",
     "piping a download straight into a shell"),
    (r"(?i)\b(iwr|invoke-restmethod|invoke-webrequest|curl)\b[^|\n]*"
     r"\|\s*(iex|invoke-expression)\b",
     "piping a download straight into PowerShell execution"),
    (r"(?i)\bcertutil\b\s+-urlcache\b", "downloading files via certutil"),
]


def check_risk(command: str) -> list:
    """Return warning descriptions for known risky command patterns.

    String matching is a warning aid, not a security boundary; shell
    syntax is complex and this list cannot catch everything.
    """
    import re

    warnings = []
    for pattern, description in RISK_PATTERNS:
        if re.search(pattern, command):
            warnings.append(description)
    return sorted(set(warnings))


# --- Display ---------------------------------------------------------------

def show_commentary(text: str) -> None:
    print(HEADER_WHISPER)
    print(style(text, "\033[3m"))


def show_explanation(text: str) -> None:
    print(HEADER_ARCHIVIST)
    print(style(text, "\033[3m"))


def show_warnings(warnings: list) -> None:
    print(HEADER_WARNING)
    for warning in warnings:
        print("  Risk detected: " + warning + ".")
    print("  Inspect the target before proceeding.")


def show_ai_error(message: str) -> None:
    print(style("(the static thickens... the ghost's voice fails)", DIM))
    print(style(message, YELLOW))


# --- Confirmation and execution ----------------------------------------------

def confirm_execute(command: str, warnings: list) -> bool:
    """Ask the user whether to run their exact command. Defaults to No."""
    show = style(command, BOLD)
    if warnings:
        show_warnings(warnings)
    print("Command: " + show)
    answer = input("Execute this exact command? [y/N] ").strip().lower()
    if answer not in ("y", "yes"):
        print(style("The command dissolves... unsummoned.", DIM))
        return False
    if warnings:
        typed = input(
            style("This command is flagged. Type EXECUTE to confirm: ", YELLOW)
        ).strip().upper()
        if typed != "EXECUTE":
            print(style("The warning holds. Command not executed.", DIM))
            return False
    return True


def execute_command(command: str, timeout: int = 60) -> "tuple[int, str]":
    """Run the user's command in the developer's shell and capture output.

    Never call this with model-generated text.
    """
    if sys.platform == "win32":
        cmd = ["powershell", "-NoProfile", "-Command", command]
    else:
        cmd = ["/bin/sh", "-c", command]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        code = result.returncode
        out = (result.stdout or "") + (result.stderr or "")
        out = out.strip()
        if len(out) > 8000:
            out = out[:8000] + "\n... (output truncated)"
        return code, out or "(no output)"
    except subprocess.TimeoutExpired:
        return None, "The incantation was interrupted: timed out after " + str(timeout) + "s."
    except Exception as exc:
        return None, "The decaying terminal refuses: " + str(exc)
