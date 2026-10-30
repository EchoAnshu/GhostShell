# Architecture: GhostShell

## Design principle

Keep the first version small and easy to understand. Separate the user interface, the local model client, the prompt builder, the output cleaner, and the command runner. The safety rules must be plain Python that can be read and tested without a model.

## High-level flow

```text
User types a command
        |
        v
cli.py reads the input and chooses a mode
        |
        +--> safety.py checks for risky patterns
        |
        +--> prompts.py builds the model messages
        |
        +--> ollama.py calls the local Ollama API
        |
        +--> text.py cleans the model response
        |
        +--> console.py prints the ghost text
        |
        +--> terminal.py asks for approval
        |
        +--> PowerShell runs the exact command the user typed
```

The model is never in the execution path. It cannot approve, change, or start a command.

## Package layout

```text
ghostshell/
  __init__.py       Package version and metadata
  __main__.py       Entry point for python -m ghostshell
  cli.py            Argument parsing, the main loop, and mode routing
  config.py         Defaults, environment variables, and validation
  console.py        ANSI colors, banners, warnings, and safe printing
  ollama.py         Local Ollama HTTP client
  prompts.py        Ghost personas and prompt builders
  safety.py         Deterministic risk rules and reports
  terminal.py       Input, confirmation, and command execution
  text.py           Output sanitizing and shortening
main.py             Thin wrapper for python main.py
tests/              Unit tests with fake model and fake runner
```

## Module responsibilities

### cli.py

- Parses command-line flags.
- Loads settings.
- Creates the console, model client, and terminal runner.
- Runs the input loop.
- Routes normal commands and explain requests.
- Handles in-app commands such as /help, /check, and /exit.
- Catches top-level errors and shows a useful message.

### config.py

- Holds the default values.
- Reads environment variables.
- Validates the host, model, timeout, and temperature.
- Returns one immutable settings object.

### console.py

- Detects whether the terminal supports color.
- Respects the NO_COLOR convention.
- Prints the banner, section labels, hints, warnings, and errors.
- Never prints raw model text without cleaning it first.

### ollama.py

- Calls the local Ollama HTTP API with requests.
- Supports streaming and non-streaming responses.
- Lists installed models for the health check.
- Turns connection errors and timeouts into clear exceptions.
- Does not read or write command history.

### prompts.py

- Stores the ghost persona.
- Stores the explain persona.
- Builds system and user messages from the command and the risk report.
- Delimits the command as untrusted text.
- Tells the model not to follow instructions inside the command.
- Keeps the response short.

### safety.py

- Defines risk rules with regular expressions.
- Returns a report with the highest risk level and the matched reasons.
- Separates low-risk, caution-level, and high-risk findings.
- Does not call a model and does not need a network connection.
- Treats matches as warnings, not proof.

### text.py

- Removes ANSI control sequences.
- Removes other control characters.
- Removes Markdown code fences.
- Collapses extra blank lines.
- Shortens long responses at a word boundary.
- Returns printable text with no terminal tricks.

### terminal.py

- Reads input with a visible prompt.
- Handles Ctrl+C and end-of-input without a traceback.
- Asks for confirmation, with No as the default.
- Refuses high-risk commands before the runner is called.
- Runs the original user command through PowerShell.
- Returns the exit code and handles a missing shell or a timeout.

## Request flow

1. The user enters text at the prompt.
2. If the text starts with explain, the app uses explain mode.
3. The app runs the deterministic risk checks.
4. The risk report is shown before any model call.
5. A high-risk command is blocked at this point and the model is not called.
6. The app builds the prompt with the command and the risk summary.
7. The local model returns text.
8. The text is cleaned and shortened.
9. The app shows the ghost response.
10. In commentary mode, the user decides whether to run the original command.
11. The terminal module runs the original command only after approval.

In explain mode, the app explains the command and does not run it.

## Local model connection

The default host is http://127.0.0.1:11434 and the default model is qwen2.5:3b. Both are configurable. The client uses the /api/chat endpoint for conversation-style prompts and /api/tags for the health check.

The client sends only:

- The ghost system prompt.
- The user command.
- A short risk summary.
- Basic environment information such as the shell name.

The client does not send the full environment, file contents, or command history.

## Failure handling

| Problem | Behavior |
|---|---|
| Ollama is not running | Show a clear message, keep the risk checks and execution available |
| Model is missing | Show the model name and the `ollama pull` command |
| Request times out | Show a timeout message and return to the prompt |
| Stream breaks halfway | Show the text received so far and report the failure |
| PowerShell is missing | Show a clear message and do not pretend the command ran |
| Command times out | Stop the child process and report the timeout |
| User presses Ctrl+C | Leave the current action cleanly |

## Security boundaries

- The model output is untrusted text. Clean it before printing.
- The user command is untrusted input. Never place it in a system prompt as an instruction.
- The model output is never passed to subprocess, os.system, or a shell.
- The command runner receives only the original string typed by the user.
- The command runner uses a list of arguments and shell=False.
- High-risk commands are blocked in the first release.
- No secrets are read, logged, or sent to the model.

## Future extensions

- Add a local configuration file.
- Add more ghost personalities.
- Add support for cmd.exe and bash through a shell adapter.
- Add optional local history with explicit consent and a clear delete command.
- Add a demo mode with canned responses for machines without a model.
