# Project Brief — GhostShell

## 1. Overview

GhostShell is a local AI terminal companion with a spooky personality. It receives commands typed by the user, generates short contextual commentary, and can explain commands or flag potentially risky operations.

The project combines a Halloween-style experience with a practical developer tool.

## 2. Problem

Terminal commands can be intimidating for beginners, and terminal workflows are usually plain and impersonal. Cloud-based AI assistants can also require an internet connection and may expose command context to an external service.

## 3. Proposed solution

Build a lightweight Python CLI that connects to a locally running open-weight model through Ollama. The model interprets the command and produces a concise response in the voice of a fictional terminal ghost.

## 4. Target users

- Students learning command-line tools
- Developers who enjoy playful tooling
- Users who want local AI assistance
- Open-source and privacy-conscious developers

## 5. MVP objectives

1. Accept a command from the user.
2. Send command context to the local Ollama API.
3. Display a short spooky response.
4. Offer a plain-language explanation mode.
5. Identify potentially destructive commands using deterministic checks.
6. Require explicit user confirmation before executing a command.
7. Continue to work offline after dependencies and model files are installed.

## 6. Non-goals for the MVP

- An autonomous AI agent
- A replacement for PowerShell or another shell
- Remote command execution
- Cloud accounts or hosted inference
- Voice interaction
- Persistent personal memory

## 7. Success criteria

- Runs on the developer's Windows laptop.
- Generates responses using a local model.
- Works with the network disconnected after setup.
- Does not execute AI-generated commands.
- Requires confirmation before running user-entered commands.
- Gives useful output without making the terminal workflow unnecessarily slow.

## 8. Open-source value

Local inference gives users control over where command context is processed. A replaceable model makes experimentation possible, while editable prompts allow the ghost's behavior to be changed without depending on a closed AI API.

## 9. Deliverable

A working CLI demo, source code, setup instructions, a short screen recording, and a project post explaining the role of open-weight AI.
