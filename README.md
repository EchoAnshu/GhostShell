# GhostShell

A haunted terminal companion that runs on your machine.

GhostShell makes PowerShell feel alive. Type a command and a local AI model whispers a short, spooky comment. Ask for an explanation and it speaks in plain English. Before anything runs, GhostShell checks for risky patterns and asks you to approve the exact command.

No cloud account. No hidden uploads. No automatic execution. Just you, your terminal, and a ghost that lives on your computer.

## Why GhostShell

- **Local by design.** The model runs through Ollama on your own machine. Your commands do not need to leave your computer.
- **Useful, not just funny.** Get a quick explanation of a command, including the flags that matter.
- **Clear warnings.** Simple Python rules flag patterns such as recursive deletes, disk formatting, shutdown commands, and download-and-run pipelines.
- **You stay in control.** The AI may comment. It never runs, rewrites, or approves a command. You approve the exact command that will run.
- **Offline after setup.** Once the model is downloaded, the core experience works without an internet connection.
- **Light on your machine.** A small Python CLI, a local model, and plain ANSI colors. No browser, no account, no heavy framework.

## A quick look

```text
> git status

[ THE GHOST WHISPERS ]
The repository is restless. Something has changed in the dark.

Run this command? [y/N] n
```

```text
> explain git log --oneline

[ THE GHOST EXPLAINS ]
This shows the commit history in a short form.
Each commit appears on one line with its short hash and message.
```

```text
> Remove-Item -Recurse .\build

[ WARNING: RESTLESS SPIRIT ]
This can delete the build folder and everything inside it.
Check the path before you continue.

GhostShell will not run this command.
```

## Features

- Short, context-aware ghost commentary for the command you typed.
- An explain mode for beginner-friendly descriptions and important flags.
- Deterministic risk checks that do not depend on the model.
- A confirmation step before execution, with No as the default answer.
- Clear messages when Ollama is not running, the model is missing, or a request fails.
- A small health check command for setup problems.
- Local-only inference and no command history stored on disk.
- Clean output that removes terminal escape sequences and control characters from model text.

## Safety promise

GhostShell follows one rule above all others:

**The AI may talk about a command. It may never run a command.**

- The only executable input is the command you typed.
- GhostShell shows that exact command before it asks for approval.
- The default answer is No.
- High-risk commands are blocked in the first release.
- Risk checks are ordinary code, not model guesses.
- The model cannot change the command, approve it, or start a shell.

Read [docs/SAFETY.md](docs/SAFETY.md) for the full policy.

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running
- A local model, for example `qwen2.5:3b`
- PowerShell 5.1 or PowerShell 7

## Setup

These commands describe the first release. The source code is planned for the next branch, and this README will be updated when the build is ready to install.

```powershell
git clone <repository-url>
cd ghostshell

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
ollama pull qwen2.5:3b

python main.py
```

If PowerShell blocks the virtual environment activation script, run this for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate the environment again.

## Usage

Start GhostShell from an activated virtual environment:

```powershell
python main.py
```

Type a command to get a ghost comment and an execution prompt.

Use explain mode to learn what a command does without running it:

```text
> explain Get-ChildItem -Force
```

Useful in-app commands:

```text
/help      Show the help text
/check     Check Ollama and the selected model
/exit      Leave GhostShell
```

## Configuration

GhostShell reads a few environment variables and command-line flags:

| Setting | Environment variable | Default |
|---|---|---|
| Ollama host | `GHOSTSHELL_HOST` | `http://127.0.0.1:11434` |
| Model | `GHOSTSHELL_MODEL` | `qwen2.5:3b` |
| Request timeout | `GHOSTSHELL_TIMEOUT` | `30` |
| Temperature | `GHOSTSHELL_TEMPERATURE` | `0.8` |
| Streaming | `GHOSTSHELL_STREAM` | `1` |
| Color | `NO_COLOR` | unset |

Command-line flags override the environment:

```powershell
python main.py --model qwen2.5:0.5b
python main.py --no-stream --no-color
```

See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for details.

## How it works

```text
You type a command
        |
        v
Deterministic risk checks
        |
        v
Ollama on your machine
        |
        v
Safe, short ghost text
        |
        v
You approve the exact command
        |
        v
PowerShell runs the command you typed
```

The model is never in the execution path. Full details are in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Project status

GhostShell is in active development. The documentation and architecture are ready. The first working CLI is the next milestone.

Planned first release:

- Working comment and explain modes.
- Deterministic risk checks.
- User-approved execution.
- Health check mode.
- Automated tests for the safety layer and the no-AI-execution rule.

## Documentation

- [Documentation index](docs/README.md)
- [Project brief](docs/PROJECT_BRIEF.md)
- [Features](docs/FEATURES.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Technology stack](docs/TECH_STACK.md)
- [Safety and privacy](docs/SAFETY.md)
- [Development guide](docs/DEVELOPMENT.md)
- [Testing guide](docs/TESTING.md)
- [Configuration](docs/CONFIGURATION.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## License

A license will be added before the first public release.
