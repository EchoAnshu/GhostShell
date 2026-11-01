# GhostShell 👻

**Something is watching your terminal.**

GhostShell is an offline-first, AI-powered haunted terminal companion. Type a command, a locally running open-weight model whispers eerie-but-useful commentary, and execution stays entirely in your hands.

```text
> git push origin main

[ THE GHOST WHISPERS ]
Sending your work into the void?
At least the void has version control.
```

## Setup

```powershell
ollama pull qwen2.5:3b

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

python main.py
```

Keep Ollama running while GhostShell is active. After the model and dependencies are downloaded, inference works offline.

## Usage

Anything you type is treated as a shell command. Meta commands:

| Command | Action |
|---|---|
| `explain <command>` | Plain-language explanation instead of commentary |
| `help` | Show the meta list |
| `exit`, `quit` | Leave the terminal |

Before every execution GhostShell shows the exact command and asks `Execute this exact command? [y/N]` — the default is `y/N` no, and commands flagged by the deterministic risk checks additionally require typing `EXECUTE`.

## Configuration

All configuration is via environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `GHOSTSHELL_HOST` | `http://localhost:11434` | Ollama API host |
| `GHOSTSHELL_MODEL` | `qwen2.5:3b` | Any model you have pulled |
| `GHOSTSHELL_TIMEOUT` | `90` | Seconds before a model request times out |
| `GHOSTSHELL_TEMPERATURE` | `0.8` | Model sampling temperature |

## Safety

The AI may comment, but it never decides and never runs anything. Model-generated text is never passed to a shell; only your confirmed, exact command executes. Risk checks are deterministic pattern matching in plain code, not model judgment. See [docs/SAFETY.md](docs/SAFETY.md).

## Project layout

```text
ghostshell/
├── main.py          # Entry point and interaction loop
├── ai.py            # Ollama HTTP API client and config
├── terminal.py      # Display, risk checks, confirmation, execution
├── prompts.py       # Ghost persona and prompt builders
├── requirements.txt
├── README.md
├── tests/
│   └── test_safety_and_prompts.py
└── docs/
    ├── PROJECT_BRIEF.md
    ├── ARCHITECTURE.md
    ├── TECH_STACK.md
    ├── FEATURES.md
    ├── README.md
    └── SAFETY.md
```

## Tests

```powershell
python -m unittest discover -s tests -t .
```

## Notes on licensure

GhostShell runs whatever open-weight model you configure; check the model's own license before redistribution. See [docs/README.md](docs/README.md).
