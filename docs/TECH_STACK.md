# Technology Stack: GhostShell

## Core stack

| Layer | Technology | Role |
|---|---|---|
| Language | Python 3.10+ | Application logic |
| Local model runtime | Ollama | Runs the model on the user's machine |
| Default model | qwen2.5:3b | Short commentary and explanations |
| Model interface | Ollama HTTP API | Connects Python to the local model |
| Shell | Windows PowerShell | Runs approved user commands |
| Terminal output | ANSI escape codes | Color and layout without a heavy library |
| HTTP client | requests | Calls the local Ollama API |
| Tests | pytest | Unit tests and safety checks |
| Lint and format | ruff | Fast checks and consistent style |

## Why Python

Python is easy to read, quick to change, and has everything this project needs: HTTP requests, process execution, text handling, and a good testing story. The app is small, so a compiled language would add build steps without helping the user.

## Why Ollama

Ollama gives a simple local API for running open-weight models. It handles model downloads, keeps the model on the user's machine, and works without a cloud account. It is also easy to replace if the user wants a different model.

## Why qwen2.5:3b as the starting model

It is small enough to run on a normal laptop and strong enough for short comments and basic explanations. The model name is a setting, so users can switch to a smaller or larger model.

Suggested options:

- qwen2.5:0.5b for low-end machines and quick demos.
- qwen2.5:3b for the default balance of speed and quality.
- A larger model for better explanations if the machine has enough memory.

## Why requests

The Ollama API is a simple HTTP JSON API. requests is stable, familiar, and has clear timeout and streaming support. The project does not need an async stack for a single-user CLI.

## Why ANSI instead of a TUI library

The interface is a prompt, a few short sections, and some warnings. A full-screen UI library would add weight and complexity without improving the core idea. ANSI codes are enough, and the app can turn color off when the terminal does not support it.

## Why PowerShell first

The owner develops on Windows and uses PowerShell. The command runner is isolated so other shells can be added later without changing the model or safety code.

## Dependencies

Runtime:

- requests

Development:

- pytest
- pytest-cov
- ruff

The standard library covers argument parsing, dataclasses, subprocess handling, Unicode cleaning, and terminal input.

## Configuration

Configurable values:

- Ollama host URL
- Model name
- Request timeout
- Temperature
- Streaming on or off
- Color on or off

Environment variables and command-line flags are described in [CONFIGURATION.md](CONFIGURATION.md).

## Model flexibility

The model name is read from settings. Switching models should not require a code change. The app checks /api/tags and shows a clear message when the selected model is not installed.

Before redistributing a model or bundling it with the project, check the model license and the terms of use.

## What we are not using

| Technology | Reason |
|---|---|
| A cloud AI API | Breaks the local-first promise |
| An async framework | Unnecessary for a single-user CLI |
| A full TUI framework | Too much weight for this interface |
| An autonomous agent framework | Against the core safety rule |
| A database | No history is stored by default |
| Electron or a web UI | The product belongs in the terminal |
