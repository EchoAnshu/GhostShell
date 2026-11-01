"""Communication with the local Ollama HTTP API for GhostShell."""

import os

import requests

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:3b"


class GhostShellAIError(Exception):
    """Base class for AI-related failures with a user-readable message."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AIUnavailable(GhostShellAIError):
    """Ollama is not reachable or returned an unexpected error."""


class AIModelMissing(GhostShellAIError):
    """The configured model is not downloaded in Ollama."""


class AITimeout(GhostShellAIError):
    """The model request took too long."""


def load_config() -> dict:
    """Configuration from environment variables with sensible defaults."""
    return {
        "host": os.environ.get("GHOSTSHELL_HOST", DEFAULT_HOST).rstrip("/"),
        "model": os.environ.get("GHOSTSHELL_MODEL", DEFAULT_MODEL),
        "timeout": float(os.environ.get("GHOSTSHELL_TIMEOUT", "90")),
        "temperature": float(os.environ.get("GHOSTSHELL_TEMPERATURE", "0.8")),
    }


def generate(messages, config=None, max_tokens=None) -> str:
    """Send messages to the local model and return its reply text."""
    cfg = config or load_config()
    options = {"temperature": cfg["temperature"]}
    if max_tokens:
        options["num_predict"] = int(max_tokens)
    payload = {
        "model": cfg["model"],
        "messages": messages,
        "stream": False,
        "options": options,
    }
    try:
        response = requests.post(
            cfg["host"] + "/api/chat",
            json=payload,
            timeout=(5, cfg["timeout"]),
        )
    except requests.exceptions.Timeout:
        raise AITimeout(
            "The spirits kept us waiting and the request timed out. "
            "(You can retry or continue without commentary.)"
        )
    except requests.exceptions.ConnectionError:
        raise AIUnavailable(
            "Ollama is not reachable at " + cfg["host"]
            + ". Start Ollama, or the ghost stays silent (no AI analysis "
            "happened; nothing was sent anywhere)."
        )

    if response.status_code == 404:
        raise AIModelMissing(
            "Model '" + cfg["model"] + "' is not downloaded in Ollama. "
            "Run: ollama pull " + cfg["model"]
        )
    if not response.ok:
        raise AIUnavailable(
            "Ollama returned HTTP " + str(response.status_code)
            + ": " + response.text[:300]
        )

    try:
        data = response.json()
    except ValueError as exc:
        raise AIUnavailable("Ollama returned a response we could not read.") from exc

    content = data.get("message", {}).get("content", "")
    if not content:
        raise GhostShellAIError("The ghost had nothing to say (empty model response).")
    return content.strip()
