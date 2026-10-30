# Testing Guide

## Goals

The tests protect the parts that matter most:

1. The AI never executes a command.
2. The command runner receives only the original user command.
3. Risky patterns produce the expected warning level.
4. Model output cannot inject terminal control sequences.
5. The app fails clearly when Ollama or the model is missing.

The tests must not need a real model, a network connection, or a real PowerShell session. Use fakes for the model client and the command runner.

## Test commands

```powershell
pytest
pytest --cov=ghostshell --cov-report=term-missing
ruff check .
ruff format --check .
```

## Test layout

```text
tests/
  test_config.py
  test_safety.py
  test_prompts.py
  test_text.py
  test_ollama.py
  test_terminal.py
  test_cli.py
```

## What each test file covers

### test_config.py

- Default values are correct.
- Environment variables override defaults.
- Command-line flags override environment variables.
- Invalid timeout and temperature values are rejected.
- Color can be turned off.

### test_safety.py

- Low-risk commands return a low report.
- Recursive deletes return a caution or high report.
- Disk format commands return a high report.
- Shutdown commands return a high report.
- Download-and-run pipelines return a high report.
- Every rule has a reason and a level.
- Empty input returns a low report.
- Case and spacing variants still match.

### test_prompts.py

- The command is placed inside a delimiter.
- The system prompt tells the model to ignore instructions in the command.
- The risk summary is included.
- Explain mode uses a different instruction from comment mode.
- A very long command is shortened before it is sent.
- The prompt does not include secrets or environment data.

### test_text.py

- ANSI escape sequences are removed.
- Control characters are removed.
- Markdown code fences are removed.
- Extra blank lines are collapsed.
- Long text is shortened at a word boundary.
- Normal text is left readable.

### test_ollama.py

- A successful chat request returns clean text.
- A connection error becomes a clear app error.
- A timeout becomes a clear app error.
- A missing model becomes a clear app error.
- A streaming response is assembled in order.
- An empty response becomes a clear app error.

### test_terminal.py

- The confirmation prompt defaults to No.
- An empty answer does not run the command.
- A yes answer calls the runner once with the original command.
- A no answer does not call the runner.
- A high-risk command is blocked before the runner is called.
- The command is passed to PowerShell without shell=True.
- A nonzero exit code is returned and shown.
- Ctrl+C is handled without a traceback.

### test_cli.py

- The banner appears on start.
- /help prints the command list.
- /exit leaves the loop.
- /check reports the model status.
- Explain mode does not call the runner.
- Comment mode asks for approval.
- An Ollama failure does not crash the app.
- Model output is cleaned before printing.

## Manual test script

Use a machine with Ollama and the selected model installed.

1. Start the app.
2. Confirm the banner and prompt appear.
3. Run `/check` and confirm it names the host and model.
4. Enter `git status`. Confirm a ghost comment appears and the approval prompt shows the exact command.
5. Press Enter. Confirm nothing runs.
6. Enter `explain git log --oneline`. Confirm an explanation appears and nothing runs.
7. Enter `Remove-Item -Recurse .\build`. Confirm a warning or block appears.
8. Enter `Remove-Item .\test-file.txt`. Confirm a caution warning appears and the command runs only after a yes.
9. Stop Ollama and repeat step 4. Confirm the app shows a clear error and still allows a normal approved command to run.
10. Select a model that is not installed. Confirm the app names the model and shows the pull command.
11. Press Ctrl+C at the prompt. Confirm the app exits without a traceback.
12. Disconnect the network after setup. Repeat steps 4 and 6. Confirm both still work with the local model.

## Safety test rules

- Add a test with every new risk rule.
- Add a test for every new path that can reach the command runner.
- Never mock away the rule that separates model output from execution.
- Assert that the runner is called with the original command, not model text.
- Assert that the runner is not called in explain mode.
- Keep the default answer test in place. It protects an important choice.

## Test style

- Use clear test names that describe the behavior.
- One behavior per test.
- Use small helper functions for repeated setup.
- Prefer plain assertions over mocking frameworks when possible.
- Use a fake model client that returns fixed text.
- Use a fake runner that records its calls.
- Do not call a real model in unit tests.

## What is not covered yet

- Visual color checks.
- Full shell parsing.
- Windows Terminal edge cases.
- Other shells.
- A real model's response quality.

These are manual checks or future test work.
