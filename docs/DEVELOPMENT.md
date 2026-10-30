# Development Guide

## Before you start

- Windows 10 or Windows 11.
- Python 3.10 or newer.
- Ollama installed and running.
- A local model downloaded.
- Git.

## First setup

```powershell
git clone https://github.com/EchoAnshu/GhostShell.git
cd ghostshell

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements-dev.txt
ollama pull qwen2.5:3b
```

If PowerShell blocks the activation script for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the app

```powershell
python main.py
```

or:

```powershell
python -m ghostshell
```

## Run a health check

```powershell
python main.py --check
```

## Run the tests

```powershell
pytest
```

With coverage:

```powershell
pytest --cov=ghostshell --cov-report=term-missing
```

## Lint and format

```powershell
ruff check .
ruff format .
```

## Project layout

```text
ghostshell/
  __init__.py
  __main__.py
  cli.py
  config.py
  console.py
  ollama.py
  prompts.py
  safety.py
  terminal.py
  text.py
main.py
tests/
docs/
pyproject.toml
requirements.txt
requirements-dev.txt
README.md
```

## Coding rules

- Keep functions small and give them clear names.
- Put business rules in modules, not in the command loop.
- Use type hints for public functions.
- Avoid global mutable state.
- Do not print from deep inside the model client. Return text and let the console print it.
- Never pass model output to a shell.
- Keep every risky action behind an explicit function with tests.
- Add a test when you add a safety rule.
- Do not add a dependency unless the standard library cannot do the job.
- Do not use em dashes in code, comments, docs, or commit messages.
- Do not use emojis in code, comments, docs, or terminal output.
- Keep public docs in simple English.

## Branch and commit workflow

1. Start from an up-to-date main.
2. Create one branch for one feature.
3. Make small commits with clear messages.
4. Push the branch.
5. Stop and wait for review.
6. Do not merge branches. The owner merges them.

Do not use the word phase in a branch name or a commit message.

Example branch names:

```text
docs/project-foundation
feat/local-ghost-cli
feat/first-run-polish
fix/ollama-timeout
```

Example commit messages:

```text
docs: rewrite the project brief in simple English
feat: add deterministic risk checks
test: cover recursive delete warnings
fix: handle an empty model response
```

## Local memory folder

The repository has a private memory folder that is ignored by Git. It contains:

- The owner's working rules.
- The idea and research notes.
- The roadmap.
- Session logs.

Read `memory/memory.md` before starting a new session. Update it when the project changes. Never commit the memory folder.

## Logging

Every session must add an entry to `memory/logs/` with:

- Commands that changed the machine or the repository.
- Packages installed or removed.
- Files created, moved, or rewritten.
- Checks that ran and their results.
- Decisions and open questions.

## Manual checks before opening a branch for review

- `pytest` passes.
- `ruff check .` passes.
- `ruff format --check .` passes.
- The app starts and shows the banner.
- `/check` reports the Ollama status.
- A normal command gets a comment.
- An explain request gets an explanation and does not run the command.
- A risky command is blocked or warned.
- The user command runs only after a yes.
- Pressing Enter at the confirmation prompt does not run anything.
- Ctrl+C leaves the app cleanly.
- The README and docs still match the code.
