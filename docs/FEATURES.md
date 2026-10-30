# Features: GhostShell

## First release

### 1. Haunted commentary

The user types a command. GhostShell sends it to a local model and prints a short ghost comment. The comment should be relevant to the command, a little eerie, and no longer than a few sentences.

### 2. Explain mode

The user can ask for a plain-language explanation of a command. The explanation should describe what the command does and mention important flags when practical. Explain mode does not run anything.

### 3. Risk warnings

Ordinary Python rules check for known risky patterns. The model is not the safety layer. Examples:

- Recursive deletion.
- Disk formatting or disk clearing.
- Shutdown or restart commands.
- Privilege escalation.
- Downloading content and running it in a shell.
- Force pushing or hard resetting a Git repository.
- Deleting registry keys or scheduled tasks.

A warning does not prove that a command is unsafe. A missing warning does not prove that a command is safe.

### 4. User-controlled execution

GhostShell shows the exact command that would run, then asks for approval. The default answer is No. High-risk commands are blocked in the first release.

The AI cannot approve, change, or run a command.

### 5. Local inference with an open model

The model runs through Ollama on the user's machine. The app does not call a cloud AI service. After the model is downloaded, the core experience works without an internet connection.

The open-weight model is the core of the product, not a side feature:

- The default model is qwen2.5:3b, and the user can change it.
- The app needs no account and no API key.
- The user can pick a smaller model for speed or a larger model for better answers.
- There is no per-request bill.

### 6. Clear errors

GhostShell explains when:

- Ollama is not running.
- The model is missing.
- A request times out.
- The shell cannot be started.
- A command exits with an error.

### 7. Health check

A check command shows the Ollama version, the selected model, and whether the model is available. This makes setup problems easier to diagnose.

### 8. Safe terminal output

Model text is cleaned before it is printed:

- Terminal escape sequences are removed.
- Control characters are removed.
- Markdown code fences are removed.
- Very long responses are shortened.

## Example interactions

### Commentary

```text
> git status

[ THE GHOST WHISPERS ]
The repository is restless. Something has changed in the dark.

Run this command? [y/N]
```

### Risky command

```text
> Remove-Item -Recurse .\build

[ WARNING: RESTLESS SPIRIT ]
This can delete the build folder and everything inside it.
Check the path before you continue.

GhostShell will not run this command.
```

### Explain mode

```text
> explain Get-ChildItem -Force

[ THE GHOST EXPLAINS ]
This lists the items in the current folder.
The -Force flag also shows hidden files and folders.
```

### Help

```text
> /help

Commands:
  explain <command>   Explain a command without running it
  /help               Show this help
  /check              Check Ollama and the selected model
  /exit               Leave GhostShell
```

## Later features

- More ghost personalities.
- Named response styles.
- A local configuration file.
- A session summary at exit.
- Support for cmd.exe and bash.
- Optional local history with clear consent.
- A demo mode with canned responses for machines without a model.

## Out of scope

- Autonomous command execution.
- Remote shell access.
- Hidden collection of command history.
- Sending command data to a cloud AI service.
- Voice interaction.
