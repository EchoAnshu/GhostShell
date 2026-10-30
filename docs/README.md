# GhostShell Documentation

Start with the project brief, then read the architecture and safety documents before changing the code.

## Core documents

- [Project brief](PROJECT_BRIEF.md): the problem, the users, the goals, and the non-goals.
- [Features](FEATURES.md): what the first release includes and what comes later.
- [Architecture](ARCHITECTURE.md): the modules, the request flow, and the failure handling.
- [Technology stack](TECH_STACK.md): the tools we use and why we use them.
- [Safety and privacy](SAFETY.md): the rules that keep the AI away from command execution.

## Working documents

- [Development guide](DEVELOPMENT.md): how to set up the project and make a change.
- [Testing guide](TESTING.md): how to run the tests and check the app by hand.
- [Configuration](CONFIGURATION.md): settings and command-line flags.
- [Troubleshooting](TROUBLESHOOTING.md): fixes for common setup problems.
- [Decisions](DECISIONS.md): the important choices and the reasons behind them.
- [Changelog](CHANGELOG.md): what changed in each release.
- [Handover](HANDOVER.md): how to pick up the project and continue.

## Reading order for a new contributor

1. [Project brief](PROJECT_BRIEF.md)
2. [Safety and privacy](SAFETY.md)
3. [Architecture](ARCHITECTURE.md)
4. [Development guide](DEVELOPMENT.md)
5. [Testing guide](TESTING.md)

## Simple summary

GhostShell is a Python command-line tool with open AI at its core. It sends the text of a command you typed to a local open-weight model through Ollama, shows a short ghost comment, and optionally explains the command. A separate safety module checks for risky patterns. The command runs only after you approve the exact command. The model is never allowed to run anything.
