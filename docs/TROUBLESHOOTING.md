# Troubleshooting

## PowerShell will not activate the virtual environment

Symptom:

```text
cannot be loaded because running scripts is disabled on this system
```

Fix for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This change lasts only for that terminal window.

## The ollama command is not found

Check the install:

```powershell
ollama --version
```

If the command is missing, install Ollama from https://ollama.com/ and open a new terminal so the PATH is updated.

## Ollama is not running

Symptom: GhostShell reports a connection error.

Check the service:

```powershell
ollama list
```

If that fails, start Ollama from the Start menu or run:

```powershell
ollama serve
```

Then try `/check` in GhostShell.

## The model is missing

Symptom: GhostShell reports that the model is not installed.

List installed models:

```powershell
ollama list
```

Download the default model:

```powershell
ollama pull qwen2.5:3b
```

Or choose an installed model:

```powershell
python main.py --model <model-name>
```

## Replies are slow

- Use a smaller model, for example qwen2.5:0.5b.
- Close other programs that use a lot of memory.
- Use --no-stream if partial output makes the terminal feel stuck.
- Raise the timeout if the first response is slow while the model loads.

The first request after a model loads is often slower than later requests.

## Replies are strange or too long

- Lower the temperature.
- Try a different model.
- Keep the command short.
- Use explain mode for a focused answer.

The model is a small local model, not a cloud service. It can be wrong. Treat its text as commentary, not as a source of truth.

## Colors look wrong

Use --no-color or set NO_COLOR:

```powershell
$env:NO_COLOR = "1"
python main.py
```

## Garbled characters

Use Windows Terminal or PowerShell 7. Set UTF-8 for the session if needed:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```

## The model starts but the command does not run

- Check the confirmation prompt. The default answer is No.
- A high-risk command is blocked by design.
- A caution-level command needs a clear yes.
- Check that PowerShell is available.
- Check that the command exists in the current PATH.

GhostShell does not hide the reason. Read the message above the prompt.

## The command runs but the shell reports an error

GhostShell runs the exact command you approved. The error is from PowerShell, not from the model. Read the shell output and check the command, the path, and your permissions.

## A warning appears for a safe command

The risk rules use patterns, not a full shell parser. A pattern can match a safe command. Read the reason, check the command, and decide for yourself.

## No warning appears for a risky command

The rules cannot catch every risky command. A clean report is not proof of safety. Check the command before you approve it.

## The app exits when I press Ctrl+C

That is the expected way to leave. If it exits during a model request, start the app again. No history is lost because no history is stored.

## A request times out

- Check that Ollama is running.
- Try a smaller model.
- Raise the timeout with --timeout.
- Check the host setting if Ollama uses a different port.

## I want to remove the model

```powershell
ollama rm qwen2.5:3b
```

## I want to remove the app

Delete the project folder and its virtual environment. No system-wide service is installed. The model stays in Ollama until you remove it with `ollama rm`.
