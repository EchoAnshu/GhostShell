# Handover

## Current state

- The repository exists on the local machine.
- The documentation set is written and committed on docs/project-foundation.
- The branch has a series of reviewable commits, starting at f689056.
- The private memory folder contains the working rules, research, roadmap, and session log.
- No application code has been written yet.
- No remote repository has been connected.
- No branch has been pushed because there is no remote.

## What exists

```text
C:\theGhostShell\ghostshell
  .editorconfig
  .gitattributes
  .gitignore
  README.md
  docs/
    README.md
    PROJECT_BRIEF.md
    FEATURES.md
    ARCHITECTURE.md
    TECH_STACK.md
    SAFETY.md
    DEVELOPMENT.md
    TESTING.md
    CONFIGURATION.md
    TROUBLESHOOTING.md
    DECISIONS.md
    CHANGELOG.md
    HANDOVER.md
  memory/            (local only, ignored by Git)
```

## Environment on the owner's machine

- Windows with PowerShell.
- Python 3.13.5.
- pip 25.1.1.
- Git 2.52.0.
- Ollama 0.40.13 at http://127.0.0.1:11434.
- No model installed at the time of this handover.
- No GitHub remote connected.

## Next branch

Create `feat/local-ghost-cli` from main after the documentation branch is reviewed.

Suggested order:

1. Add `pyproject.toml`, `requirements.txt`, and `requirements-dev.txt`.
2. Add the `ghostshell` package and `main.py`.
3. Add config loading.
4. Add the Ollama client.
5. Add prompt building.
6. Add the safety rules.
7. Add the output cleaner.
8. Add the console.
9. Add the terminal runner.
10. Add the CLI loop.
11. Add tests as each module lands.
12. Update the README with the real setup steps.

## First code branch acceptance checks

- `python main.py` starts and shows the banner.
- `/check` reports Ollama and the model.
- A normal command gets a ghost comment.
- Explain mode explains and does not run.
- A risky command is blocked or warned.
- The default answer at the confirmation prompt is No.
- Model text is cleaned before printing.
- `pytest` passes.
- `ruff check .` passes.
- `ruff format --check .` passes.

## Important rules for the next person

- Read `memory/memory.md` first.
- Do not push the memory folder.
- Do not use em dashes or emojis.
- Do not add references to competitions, themes, or sensitive material in public docs.
- Do not let model output reach a shell.
- Ask before deleting anything.
- Stop after each branch and wait for review.
- Update the session log and the global opencode log.

## Open questions

- Which model should be the default after testing on the owner's laptop?
- Should a future release allow a typed-phrase override for high-risk commands, or keep the hard block?
- Should the app support cmd.exe in the first release?
- Should the project be published on GitHub before or after the first working build?
- What license should the project use?

## Handover checklist

- [ ] Read the project brief and safety policy.
- [ ] Read the architecture and testing guide.
- [ ] Check the environment.
- [ ] Create the next branch from main.
- [ ] Build the smallest working slice first.
- [ ] Test the no-AI-execution rule.
- [ ] Update the README and changelog.
- [ ] Stop for review.
