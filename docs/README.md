# GhostShell 👻

**Something is watching your terminal.**

GhostShell is an offline-first, AI-powered haunted terminal companion. It observes commands entered by the user, asks a locally running open-weight language model to generate eerie commentary or practical explanations, and leaves command execution under the user's control.

## Core idea

A normal terminal command gets a personality:

```text
> git push origin main

[ THE GHOST WHISPERS ]
Sending your work into the void?
At least the void has version control.
```

GhostShell is intended to be entertaining without sacrificing usefulness or safety.

## Project goals

- Run AI locally through [Ollama](https://ollama.com/).
- Work without an internet connection after the model is downloaded.
- Generate spooky, context-aware command commentary.
- Explain commands in plain language when requested.
- Warn about potentially destructive commands.
- Never execute AI-generated commands automatically.

## Planned technology

- Python
- Ollama local API
- Qwen2.5 3B (initial model; replaceable)
- PowerShell on Windows for the first version
- ANSI terminal styling

## Requirements

- Python 3.10+
- Ollama installed and running
- A compatible model downloaded locally, for example:

```powershell
ollama pull qwen2.5:3b
```

## Initial setup

```powershell
git clone <your-repository-url>
cd ghostshell

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt
ollama run qwen2.5:3b
```

Keep Ollama running, then start GhostShell in another terminal:

```powershell
python main.py
```

> These commands run the implemented application. `requirements.txt` pins `requests`; everything else is standard library.

## Planned project structure

```text
ghostshell/
├── main.py          # Application entry point and interaction loop
├── ai.py            # Communication with the local Ollama API
├── terminal.py      # Command input and controlled execution
├── prompts.py       # Ghost persona and prompt instructions
├── requirements.txt
├── README.md
└── docs/
    ├── PROJECT_BRIEF.md
    ├── ARCHITECTURE.md
    ├── TECH_STACK.md
    ├── FEATURES.md
    └── SAFETY.md
```

## Open innovation

GhostShell uses an open-weight model through a locally hosted inference runtime. This makes model choice, prompting, inference location, and future customization controllable by the user. Terminal input and output do not need to be sent to a third-party AI service.

Check the model's license and usage terms before redistribution or deployment.

## Safety

GhostShell is an assistant, not an autonomous shell agent. It must not run commands suggested by the model. The user reviews and explicitly confirms every command before execution. See [SAFETY.md](docs/SAFETY.md).

## Current status

**MVP implemented.** `main.py`, `ai.py`, `terminal.py`, and `prompts.py` are in place: haunted commentary and explain modes, deterministic risk warnings, confirmation-gated execution through a controlled PowerShell/subprocess interface, Ollama connection errors surfaced honestly, and configuration via `GHOSTSHELL_*` environment variables.

Run the checks with:

```powershell
python -m unittest discover -s tests -t .
```

Still open: multiple ghost personalities, optional local command history, and tests for the execution layer. See [FEATURES.md](FEATURES.md).

## Theme

Built for **Ghost in the Machine**: a haunted terminal powered by local, open-weight AI.
