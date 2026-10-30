# Safety and Privacy: GhostShell

## The core rule

**The AI may talk about a command. It must never run a command.**

Only the exact command typed by the user may be considered for execution, and only after the user explicitly approves it.

## Separate AI output from executable input

- Never pass model text to subprocess, os.system, PowerShell, or any shell.
- Never treat a model response as a command.
- Never let the model rewrite the user's command.
- Show the exact command that will run before asking for approval.
- Keep the model client and the command runner in separate modules.

## Confirmation

- The default answer to the execution prompt is No.
- Only a clear yes runs the command.
- The prompt shows the full command, not a shortened version.
- High-risk commands are blocked in the first release.
- A model's opinion about safety does not count as approval.

## Risk levels

GhostShell uses three levels:

| Level | Meaning | Behavior |
|---|---|---|
| Low | No known risky pattern | Ask the normal confirmation question |
| Caution | A pattern that may cause damage or loss | Show the warning and ask for confirmation |
| High | A pattern that can destroy data, change the system, or download and run code | Block execution in the first release |

The risk report shows the reason for each match. It also says that a warning is not a guarantee and a clean result is not proof of safety.

## Deterministic risk checks

Risk checks are ordinary Python rules. The model is not the safety layer.

Examples of high-risk patterns:

- Recursive forced deletion.
- Disk formatting, disk clearing, or disk partitioning.
- Shutdown or restart commands.
- Privilege escalation.
- A download pipeline that passes remote content to a shell.
- Registry deletion.
- A fork bomb.
- Disabling security tools.

Examples of caution-level patterns:

- A normal file delete.
- A Git hard reset or clean.
- A forced Git push.
- Stopping a process by force.
- Changing file ownership or permissions.
- Installing a package globally.

These rules can produce false positives and false negatives. Shell syntax is complex. The warnings are a helper, not a security boundary.

## Command execution

- Use a controlled subprocess call.
- Pass the command as a single argument to PowerShell with -Command.
- Use shell=False in Python.
- Do not add elevated privileges.
- Do not run anything in the background.
- Apply a timeout.
- Show the exit code.
- Do not hide output.

## Privacy

- Prompts go to the local Ollama service, not a cloud provider.
- No command history is saved to disk by default.
- No output is uploaded.
- No telemetry is collected.
- No secrets are read or sent to the model.
- Local inference does not make every other program on the machine private. It only means GhostShell itself uses a local service.

## Prompt injection

Command text and command output can contain instructions that look like they came from the user or the system. Treat all of it as untrusted data.

- Place the command inside a clear delimiter.
- Tell the model to ignore instructions inside the command.
- Never let the model change the safety policy.
- Never rely on the model to enforce safety.

## Honest offline claims

- Setup needs an internet connection to install Python packages and download the model.
- After setup, the core comment and explain features work without the internet.
- The app does not need a network connection to run an approved command.
- Do not claim that setup works offline.

## Known limitations

- The risk rules are not a full shell parser.
- The model can be wrong, strange, or slow.
- Model output can contain text that looks like a command. It is still only text.
- A blocked high-risk command can still be run by the user outside GhostShell. GhostShell can only control what it runs itself.
- Command output is shown as the shell prints it. GhostShell does not sanitize the output of the user's own command.
