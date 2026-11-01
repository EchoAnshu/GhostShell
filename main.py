"""GhostShell entry point: the haunted interaction loop."""

import sys

import ai
import prompts
import terminal

BANNER = r"""
    .-. _______ .-.
   ( ( )  {ghostshell} ( ) )
    '-/  _____  \-'
      / |  o o|  \
      \ |  \_/|  /
      {_|   | |}|
       '-|_|_|-'
    Something is watching your terminal.
"""

HELP = """
Meta commands:
  help                 Show this list
  explain <command>    Plain-language explanation instead of commentary
  exit | quit          Release the ghost

Anything else is treated as a shell command. Commands are only
executed if you confirm each one explicitly.
"""

EXIT_WORDS = ("exit", "quit", "bye")


def classify(raw: str):
    """Return (mode, command, is_meta_help)."""
    stripped = raw.strip()
    lowered = stripped.lower()
    if lowered.startswith("explain "):
        return prompts.MODE_EXPLAIN, stripped[8:].strip(), False
    return prompts.MODE_COMMENTARY, stripped, False


def main() -> None:
    terminal.enable_ansi()
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    config = ai.load_config()
    terminal.enter_haunted_mode()
    try:
        print(HELP)
        print(
            terminal.style(
                "Local model: " + config["model"] + "  @  " + config["host"],
                terminal.DIM,
            )
        )

        while True:
            try:
                raw = input("\n" + terminal.prompt_str())
            except (KeyboardInterrupt, EOFError):
                print("\n" + terminal.style("The candle goes out. Goodbye...", terminal.DIM))
                break

            command = raw.strip()
            if not command:
                continue
            lowered = command.lower()
            if lowered in EXIT_WORDS:
                print(terminal.style("The candle goes out. Goodbye...", terminal.DIM))
                break
            if lowered in ("help", "?") or lowered == "help\n":
                print(HELP)
                continue

            mode, actual = classify(command)
            if not actual:
                print("Explain what? Usage: explain <command>")
                continue

            warnings = terminal.check_risk(actual)

            try:
                max_tokens = 45 if mode == prompts.MODE_COMMENTARY else 140
                messages = prompts.build_messages(mode, actual, warnings)
                reply = ai.generate(messages, config, max_tokens=max_tokens)
            except ai.GhostShellAIError as exc:
                terminal.show_ai_error(exc.message)
            except Exception as exc:
                terminal.show_ai_error("Unexpected ghost interference: " + str(exc))
            else:
                if mode == prompts.MODE_EXPLAIN:
                    terminal.show_explanation(reply)
                    continue
                terminal.show_commentary(reply)

            if mode == prompts.MODE_EXPLAIN:
                continue

            if terminal.confirm_execute(actual, warnings):
                code, output = terminal.execute_command(actual)
                print(output)
                if code is None:
                    pass
                else:
                    label = terminal.style("exit " + str(code), terminal.YELLOW)
                    print("(" + label + ")")
            else:
                continue
    finally:
        terminal.leave_haunted_mode()


if __name__ == "__main__":
    main()
