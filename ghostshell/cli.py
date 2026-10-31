"""Command-line interface for GhostShell."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from .config import Config, ConfigError, load_config
from .console import Console
from .ollama import OllamaClient, OllamaError
from .prompts import build_messages
from .safety import RiskReport, check_command
from .terminal import Terminal, TerminalError, TerminalTimeout
from .text import StreamSanitizer, sanitize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ghostshell",
        description="A haunted local terminal companion powered by an open-weight model.",
    )
    parser.add_argument("--host", help="Ollama API address")
    parser.add_argument("--model", help="Model name installed in Ollama")
    parser.add_argument("--timeout", type=float, help="Model request timeout in seconds")
    parser.add_argument("--temperature", type=float, help="Model temperature from 0 to 2")
    parser.add_argument(
        "--no-stream",
        dest="stream",
        action="store_false",
        default=None,
        help="Wait for the full model response",
    )
    parser.add_argument(
        "--no-color",
        dest="color",
        action="store_false",
        default=None,
        help="Turn color off",
    )
    parser.add_argument(
        "--check", action="store_true", help="Check Ollama and the model, then exit"
    )
    parser.add_argument("--version", action="store_true", help="Show the version and exit")
    return parser


def _show_report(console: Console, report: RiskReport) -> None:
    if not report.findings:
        return
    if report.blocked:
        console.warning("[ BLOCKED: RESTLESS SPIRIT ]")
    else:
        console.warning("[ WARNING: RESTLESS SPIRIT ]")
    for finding in report.findings:
        console.warning(f"- {finding.reason}")
    if report.blocked:
        console.hint("GhostShell will not run this command.")
    else:
        console.hint("A warning is not proof. Check the command before you approve it.")


def _show_status(console: Console, config: Config, client: OllamaClient) -> bool:
    try:
        status = client.status()
    except OllamaError as exc:
        console.error(str(exc))
        return False

    console.write(f"Ollama: {status.version}")
    console.write(f"Host: {config.host}")
    console.write(f"Model: {config.model}")
    if status.model_installed:
        console.success("Model status: installed")
        return True
    console.warning("Model status: missing")
    console.hint(f"Run: ollama pull {config.model}")
    return False


def _generate(
    console: Console,
    client: OllamaClient,
    config: Config,
    messages: list[dict[str, str]],
) -> None:
    if not config.stream:
        text = client.chat(messages)
        console.write(sanitize(text))
        return

    sanitizer = StreamSanitizer()
    try:
        client.chat(
            messages,
            on_chunk=lambda chunk: console.write(sanitizer.feed(chunk), end=""),
        )
    finally:
        tail = sanitizer.flush()
        if tail:
            console.write(tail, end="")
        console.write()


def _handle_explain(
    console: Console,
    client: OllamaClient,
    config: Config,
    command: str,
) -> None:
    report = check_command(command)
    _show_report(console, report)
    if report.blocked:
        return

    messages = build_messages(command, "explain", report)
    console.section("THE GHOST EXPLAINS")
    try:
        _generate(console, client, config, messages)
    except OllamaError as exc:
        console.error(str(exc))


def _handle_comment(
    console: Console,
    client: OllamaClient,
    terminal: Terminal,
    config: Config,
    command: str,
) -> None:
    report = check_command(command)
    _show_report(console, report)
    if report.blocked:
        return

    messages = build_messages(command, "comment", report)
    console.section("THE GHOST WHISPERS")
    model_ok = True
    try:
        _generate(console, client, config, messages)
    except OllamaError as exc:
        console.error(str(exc))
        model_ok = False

    console.write()
    question = "Run this command?" if model_ok else "Run it without a ghost comment?"
    if not terminal.confirm(question):
        console.hint("Nothing was run.")
        return

    try:
        code = terminal.run(command)
    except TerminalTimeout as exc:
        console.error(str(exc))
        return
    except TerminalError as exc:
        console.error(str(exc))
        return
    if code != 0:
        console.error(f"The command exited with code {code}.")


def run_cli(
    config: Config,
    console: Console,
    client: OllamaClient,
    terminal: Terminal,
) -> int:
    console.banner()
    while True:
        try:
            line = terminal.read("> ")
        except EOFError:
            console.write()
            console.hint("The ghost fades.")
            return 0
        except KeyboardInterrupt:
            console.write()
            console.hint("The ghost fades.")
            return 0

        if not line:
            continue

        lower = line.lower()
        if lower in {"/exit", "/quit", "exit", "quit"}:
            console.hint("The ghost fades.")
            return 0
        if lower == "/help":
            console.help()
            continue
        if lower == "/check":
            _show_status(console, config, client)
            continue
        if lower == "explain" or lower.startswith("explain "):
            command = line[len("explain") :].strip()
            if not command:
                console.error("Type a command after explain.")
                continue
            _handle_explain(console, client, config, command)
            continue

        _handle_comment(console, client, terminal, config, line)


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(f"GhostShell {__version__}")
        return 0

    try:
        config = load_config(args)
    except ConfigError as exc:
        print(f"GhostShell: {exc}", file=sys.stderr)
        return 2

    console = Console(color=config.color)
    client = OllamaClient(config)
    terminal = Terminal()

    if args.check:
        return 0 if _show_status(console, config, client) else 1

    try:
        return run_cli(config, console, client, terminal)
    except KeyboardInterrupt:
        console.write()
        console.hint("The ghost fades.")
        return 0
