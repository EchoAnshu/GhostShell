# Project Brief: GhostShell

## What it is

GhostShell is a local AI terminal companion with a spooky personality. It reads a command typed by the user, generates a short comment in the voice of a fictional terminal ghost, and can explain the command in plain English. It also warns about risky command patterns before the user decides whether to run anything.

The ghost is the fun part. The useful part is the explanation, the warning system, and the rule that the AI never gets control of the shell.

## The problem

- The terminal can feel cold and unfriendly.
- Beginners do not always know what a command will do.
- Cloud AI assistants may send command text to another company.
- An AI agent that runs commands on its own is risky and hard to trust.
- Most terminal tools are either useful or fun, but rarely both.

## The solution

Build a small Python command-line tool that talks to a local open-weight model through Ollama. The model receives the user's command and a short, controlled prompt. It returns a short ghost comment or a beginner-friendly explanation.

A separate Python module checks for dangerous command patterns using ordinary rules. The model may add context, but it is not the safety layer. The user sees the exact command and must approve it before it runs.

## Who it is for

- Students learning PowerShell and the command line.
- Developers who enjoy playful tools.
- Privacy-conscious users who prefer local inference.
- Anyone who wants a second look before running a risky command.

## Goals

1. Accept a command from the user.
2. Send the command to a local Ollama model.
3. Show a short, relevant ghost response.
4. Offer an explanation mode for beginners.
5. Flag known risky commands with deterministic checks.
6. Require explicit approval before execution.
7. Keep the model out of the execution path.
8. Work offline after the model and dependencies are installed.
9. Keep setup and daily use simple.

## Non-goals

- An autonomous AI agent.
- A full replacement for PowerShell or another shell.
- Remote command execution.
- Cloud accounts or hosted inference.
- Voice interaction.
- Persistent personal memory.
- Remote analytics or telemetry.

## Success criteria

- The app runs on a Windows laptop with Python and Ollama installed.
- It produces a response from a local model.
- It works with the network disconnected after setup.
- It never executes model output.
- It asks for approval before running a user command.
- It gives a useful explanation without a long delay.
- It stays readable and easy to change.

## What we will deliver

- A working command-line app.
- Source code with a small, clear module structure.
- Setup and usage instructions.
- A safety policy.
- A short demo transcript that shows the main flow.
- Tests for the risky parts: safety checks, prompt building, output cleaning, and the no-AI-execution rule.
