# Features — GhostShell

## MVP

### 1. Haunted commentary
Generate a short, contextual ghost response after a user enters a command.

### 2. Explain mode
Explain what a command does in beginner-friendly language, including important flags where practical.

### 3. Risk warnings
Use deterministic rules to flag known destructive or sensitive command patterns. The language model may add context, but it must not be the only safety mechanism.

### 4. User-controlled execution
Show the command and ask the user to confirm before execution. The AI cannot approve or execute commands.

### 5. Offline inference
Use a locally installed model through Ollama. Once the model and required dependencies are downloaded, core inference should work without internet access.

### 6. Error handling
Explain when Ollama is unavailable, the model is missing, or a request fails.

## Example interactions

### Git command

```text
> git status

[ THE GHOST WHISPERS ]
The repository is restless. Check which files have changed
before you summon another commit.
```

### File deletion

```text
> Remove-Item -Recurse .\build

[ WARNING: RESTLESS SPIRIT ]
This can remove the build folder and its contents.
Inspect the target before proceeding.

Execute this exact command? [y/N]
```

### Explain mode

```text
> explain git log --oneline

[ THE ARCHIVIST SPEAKS ]
Shows the commit history with each commit condensed
to a single line.
```

## Later features

- Multiple ghost personalities
- Optional local command history
- Custom themes and terminal effects
- Configurable model selection
- Support for additional shells
- Voice interaction
- Session summaries

## Out of scope

Do not add autonomous command execution, remote shell access, or hidden collection of command history.
