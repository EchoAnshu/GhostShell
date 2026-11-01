# Safety and Privacy — GhostShell

## 1. Core rule

**The AI may comment on commands, but it must never execute commands.**

Only the user's original command may be considered for execution, and only after explicit confirmation.

## 2. Separate AI output from executable input

- Never pass model-generated text to `subprocess`, `os.system`, PowerShell, or another shell.
- Never treat a model response as a command.
- Never allow the model to silently modify the user's command.
- Display the exact command that will be executed before asking for confirmation.

## 3. Confirmation

- Default to **No** when asking whether to execute.
- Require an explicit affirmative response.
- For high-risk operations, show a clear warning and consider blocking execution in the MVP.
- Do not assume that a model's safety assessment makes a command safe.

## 4. Deterministic risk checks

Use ordinary code and explicit patterns to flag known risky operations. Examples include recursive deletion, disk formatting, shutdown, privilege changes, and commands that pipe downloaded content directly into a shell.

These checks are warnings, not a complete security boundary. Shell syntax is complex, and simple string matching can miss dangerous behavior.

## 5. Command execution

- Use a controlled subprocess interface.
- Avoid silently enabling elevated privileges.
- Do not run commands in the background without the user's knowledge.
- Set reasonable execution timeouts where possible.
- Keep the first version limited to the developer's chosen shell.

## 6. Privacy

- Send prompts to the local Ollama service, not a remote AI provider.
- Do not upload command history.
- Do not persist command input or output by default.
- Explain that local model inference does not automatically guarantee that every other application on the machine is private.

## 7. Prompt-injection awareness

Command output and files may contain text that looks like instructions. Treat this content as untrusted data. It must not override GhostShell's system instructions or safety rules.

## 8. Honest offline claims

GhostShell can perform local inference offline after the model and dependencies have been downloaded. Initial installation and model downloads require internet access. Do not claim that setup or every optional feature works offline unless tested.
