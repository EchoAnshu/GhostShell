# Decisions

This file records the important choices and the reasons behind them. Add a new entry when a choice changes.

## 1. Local open-weight model through Ollama

**Decision:** Use Ollama and a local open-weight model.

**Why:** It keeps command text on the user's machine, removes the need for an API key, and works offline after setup. It also lets the user switch models without a code change. The open model is the core of the product, not a feature added on top.

**Trade-off:** The user must install Ollama and download a model. A small model is less capable than a large cloud model.

## 2. Python for the first release

**Decision:** Build the CLI in Python.

**Why:** It is quick to read and change, has good process and HTTP support, and fits a small command-line tool. The owner is learning Python, so clear code matters more than raw speed.

**Trade-off:** A packaged binary needs extra work. The first release runs from a virtual environment.

## 3. The AI never executes commands

**Decision:** The model may only return text. The user command is the only executable input, and it runs only after approval.

**Why:** This is the core safety promise. It keeps the blast radius small and makes the tool easy to trust.

**Trade-off:** The app is less convenient than an autonomous agent. That is intentional.

## 4. Deterministic safety checks

**Decision:** Use Python rules for risk checks, not model judgment.

**Why:** Rules are testable, predictable, fast, and work offline. A model can be persuaded by text in the command.

**Trade-off:** Rules can produce false positives and false negatives. The app says so in the warning text.

## 5. No command history by default

**Decision:** Do not save commands or model responses to disk.

**Why:** Commands can contain secrets, paths, and personal data. A terminal companion should not create a hidden record.

**Trade-off:** There is no history to review or search. A future opt-in feature may add it with clear consent.

## 6. Short responses

**Decision:** Limit ghost comments and explanations to a few sentences.

**Why:** The terminal should stay readable, and a small model produces better text when the task is narrow.

**Trade-off:** A complex command may need a second request or a larger model.

## 7. ANSI instead of a TUI framework

**Decision:** Use plain ANSI codes and simple text layout.

**Why:** The interface is small. A TUI framework would add weight and reduce portability.

**Trade-off:** Less visual polish. Color can be turned off for accessibility and logs.

## 8. PowerShell first

**Decision:** Support Windows PowerShell in the first release.

**Why:** It matches the owner's machine and keeps the command runner simple.

**Trade-off:** Other shells need an adapter later. The rest of the app is shell-neutral.

## 9. High-risk commands blocked

**Decision:** Refuse high-risk commands in the first release.

**Why:** A mistyped destructive command can cause serious damage. A hard block gives the safety layer teeth.

**Trade-off:** A power user may need a separate, explicit override. The first release has no override. A future release may add a typed phrase.

## 10. Simple module layout

**Decision:** Use a small package with one job per module.

**Why:** The project is easier to test, review, and extend. It also keeps the safety boundary visible.

**Trade-off:** More files than a single script. The extra structure is worth it.

## 11. No em dashes or emojis in the codebase

**Decision:** Keep all tracked text free of em dashes and emojis.

**Why:** The owner wants a clean, plain style that reads well in a terminal and in diffs.

**Trade-off:** Some sentences need a comma, colon, or full stop instead.
