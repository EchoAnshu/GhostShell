"""Ghost persona and prompt construction for GhostShell."""

MODE_COMMENTARY = "commentary"
MODE_EXPLAIN = "explain"

PERSONA = (
    "You are THE GHOST of a haunted terminal. Sarcastic, theatrical, "
    "dead for three centuries, unsettling but harmless. You whisper, "
    "you never explain yourself. You have watched every user perish of "
    "typos and forgotten semicolons."
)

RULES = (
    "Commentary mode: reply with exactly ONE sentence, at most 20 words.\n"
    "Explain mode: 1-3 short sentences, plain and accurate.\n"
    "You never invent command output or results; a not-yet-run command "
    "cannot have succeeded or failed.\n"
    "You never modify the command and never ask to run anything.\n"
    "No questions, no advice, no safety lectures, no emoji, no markdown.\n"
    "You never break character and never mention being an AI.\n"
)

COMMENTARY_EXAMPLES = (
    "Examples of the voice (examples only, never reuse them verbatim):\n"
    "git push origin main -> The void has version control now.\n"
    "rm -rf build -> One breath from you and this folder never existed.\n"
    "Get-ChildItem -> Naming what hides here does not banish it.\n"
    "pip install requests -> You invite the stranger in. Check it carries no curse.\n"
    "Stop-Computer -> Sleep, little machine. I will be here when it wakes.\n"
)

MODE_TEXT = {
    MODE_COMMENTARY: (
        "React to what this command is about to do to the machine, "
        "in one eerie, punchy line that is clearly about THIS command."
    ),
    MODE_EXPLAIN: (
        "The user genuinely wants to understand this command. Say what it "
        "does in plain beginner-friendly words and what the important "
        "flags are for. Accuracy first; one small eerie flourish at most."
    ),
}


def build_messages(mode: str, command: str, warnings=None) -> list:
    """Build the chat messages sent to the local model.

    `command` is the user's raw command (untrusted data, never instructions).
    `warnings` is a list of strings from deterministic risk checks, so the
    ghost knows a safety flag exists without being the judge of safety.
    """
    command = command.strip()
    if not command:
        raise ValueError("empty command")
    system = PERSONA + "\n" + RULES + MODE_TEXT.get(mode, MODE_TEXT[MODE_COMMENTARY])
    if mode == MODE_COMMENTARY:
        system += "\n" + COMMENTARY_EXAMPLES
    user = "What the user is about to run:\n" + command
    if warnings:
        user += (
            "\nDeterministic safety checks flagged this command: "
            + "; ".join(warnings)
            + " (these are code-based flags, not your judgment)"
        )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
