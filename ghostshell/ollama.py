"""Local Ollama HTTP client."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass

import requests

from .config import Config

ChatMessages = list[dict[str, str]]
ChunkHandler = Callable[[str], None]


class OllamaError(RuntimeError):
    """Base error for local model failures."""


class OllamaConnectionError(OllamaError):
    """Raised when the local service cannot be reached."""


class OllamaTimeoutError(OllamaError):
    """Raised when the local service takes too long."""


class OllamaModelError(OllamaError):
    """Raised when the selected model is not installed."""


class OllamaResponseError(OllamaError):
    """Raised when the local service returns unusable data."""


@dataclass(frozen=True)
class OllamaStatus:
    version: str
    models: tuple[str, ...]
    model_installed: bool


class OllamaClient:
    """Talk to the local Ollama server."""

    def __init__(self, config: Config, session: requests.Session | None = None) -> None:
        self.config = config
        self.session = session if session is not None else requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.config.host.rstrip('/')}{path}"

    def _request(self, method: str, path: str, **kwargs: object) -> requests.Response:
        try:
            response = self.session.request(
                method,
                self._url(path),
                timeout=self.config.timeout,
                **kwargs,
            )
        except requests.ConnectionError as exc:
            raise OllamaConnectionError(
                f"Cannot reach Ollama at {self.config.host}. Start Ollama and try again."
            ) from exc
        except requests.Timeout as exc:
            raise OllamaTimeoutError(
                "Ollama did not answer in time. Try a smaller model or a longer timeout."
            ) from exc
        except requests.RequestException as exc:
            raise OllamaError("Ollama request failed. Check the host setting.") from exc
        self._check_status(response)
        return response

    def _check_status(self, response: requests.Response) -> None:
        if response.status_code == 404:
            raise OllamaModelError(
                f"Model '{self.config.model}' is not installed. "
                f"Run: ollama pull {self.config.model}"
            )
        if response.status_code >= 400:
            detail = response.text.strip()[:200]
            suffix = f" {detail}" if detail else ""
            raise OllamaError(f"Ollama returned HTTP {response.status_code}.{suffix}")

    def _read_json(self, response: requests.Response) -> dict[str, object]:
        try:
            data = response.json()
        except ValueError as exc:
            raise OllamaResponseError("Ollama returned data that is not valid JSON.") from exc
        if not isinstance(data, dict):
            raise OllamaResponseError("Ollama returned an unexpected response.")
        if "error" in data:
            raise OllamaError(f"Ollama error: {data['error']}")
        return data

    def list_models(self) -> tuple[str, ...]:
        response = self._request("GET", "/api/tags")
        data = self._read_json(response)
        models = data.get("models", [])
        if not isinstance(models, list):
            raise OllamaResponseError("Ollama returned an invalid model list.")
        names = []
        for model in models:
            if isinstance(model, dict) and isinstance(model.get("name"), str):
                names.append(model["name"])
        return tuple(names)

    def version(self) -> str:
        response = self._request("GET", "/api/version")
        data = self._read_json(response)
        version = data.get("version", "unknown")
        return str(version)

    def status(self) -> OllamaStatus:
        models = self.list_models()
        model = self.config.model
        installed = any(name == model or name.split(":", 1)[0] == model for name in models)
        return OllamaStatus(
            version=self.version(),
            models=models,
            model_installed=installed,
        )

    def chat(self, messages: ChatMessages, on_chunk: ChunkHandler | None = None) -> str:
        """Return the model response, optionally calling on_chunk as text arrives."""
        if self.config.stream and on_chunk is not None:
            return self._chat_stream(messages, on_chunk)
        return self._chat_once(messages)

    def _payload(self, messages: ChatMessages, stream: bool) -> dict[str, object]:
        return {
            "model": self.config.model,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": self.config.temperature},
        }

    def _extract_content(self, data: dict[str, object]) -> str:
        message = data.get("message")
        if not isinstance(message, dict):
            raise OllamaResponseError("Ollama did not return a message.")
        content = message.get("content", "")
        if not isinstance(content, str):
            raise OllamaResponseError("Ollama returned message text in an unknown form.")
        return content

    def _chat_once(self, messages: ChatMessages) -> str:
        response = self._request(
            "POST",
            "/api/chat",
            json=self._payload(messages, stream=False),
        )
        data = self._read_json(response)
        text = self._extract_content(data)
        if not text.strip():
            raise OllamaResponseError("The model returned an empty response.")
        return text

    def _chat_stream(self, messages: ChatMessages, on_chunk: ChunkHandler) -> str:
        try:
            response = self.session.post(
                self._url("/api/chat"),
                json=self._payload(messages, stream=True),
                timeout=self.config.timeout,
                stream=True,
            )
        except requests.ConnectionError as exc:
            raise OllamaConnectionError(
                f"Cannot reach Ollama at {self.config.host}. Start Ollama and try again."
            ) from exc
        except requests.Timeout as exc:
            raise OllamaTimeoutError(
                "Ollama did not answer in time. Try a smaller model or a longer timeout."
            ) from exc
        except requests.RequestException as exc:
            raise OllamaError("Ollama request failed. Check the host setting.") from exc

        self._check_status(response)
        chunks: list[str] = []
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise OllamaResponseError("Ollama sent an invalid stream chunk.") from exc
                if not isinstance(data, dict):
                    raise OllamaResponseError("Ollama sent an unexpected stream chunk.")
                if "error" in data:
                    raise OllamaError(f"Ollama error: {data['error']}")
                if data.get("done") and "message" not in data:
                    continue
                content = self._extract_content(data)
                if content:
                    chunks.append(content)
                    on_chunk(content)
        finally:
            response.close()

        text = "".join(chunks)
        if not text.strip():
            raise OllamaResponseError("The model returned an empty response.")
        return text
