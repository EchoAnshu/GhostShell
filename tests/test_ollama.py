import pytest
import requests

from ghostshell.config import Config
from ghostshell.ollama import (
    OllamaClient,
    OllamaConnectionError,
    OllamaError,
    OllamaModelError,
    OllamaResponseError,
    OllamaTimeoutError,
)


class FakeResponse:
    def __init__(self, status_code=200, payload=None, lines=None, text=""):
        self.status_code = status_code
        self.payload = payload if payload is not None else {}
        self.lines = lines or []
        self.text = text
        self.closed = False

    def json(self):
        return self.payload

    def iter_lines(self, decode_unicode=False):
        yield from self.lines

    def close(self):
        self.closed = True


class FakeSession:
    def __init__(self, response=None, error=None):
        self.response = response
        self.error = error
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if self.error is not None:
            raise self.error
        return self.response

    def post(self, url, **kwargs):
        self.calls.append(("POST", url, kwargs))
        if self.error is not None:
            raise self.error
        return self.response


def test_chat_returns_text():
    response = FakeResponse(payload={"message": {"content": "Boo"}})
    client = OllamaClient(Config(stream=False), FakeSession(response))
    assert client.chat([{"role": "user", "content": "hi"}]) == "Boo"


def test_chat_streams_chunks_in_order():
    response = FakeResponse(
        lines=[
            '{"message": {"content": "Boo"}}',
            '{"message": {"content": "!"}}',
            '{"done": true}',
        ]
    )
    client = OllamaClient(Config(stream=True), FakeSession(response))
    chunks = []
    text = client.chat([{"role": "user", "content": "hi"}], on_chunk=chunks.append)
    assert text == "Boo!"
    assert chunks == ["Boo", "!"]
    assert response.closed is True


def test_connection_error_is_clear():
    client = OllamaClient(Config(stream=False), FakeSession(error=requests.ConnectionError()))
    with pytest.raises(OllamaConnectionError, match="Cannot reach Ollama"):
        client.chat([{"role": "user", "content": "hi"}])


def test_timeout_is_clear():
    client = OllamaClient(Config(stream=False), FakeSession(error=requests.Timeout()))
    with pytest.raises(OllamaTimeoutError, match="did not answer"):
        client.chat([{"role": "user", "content": "hi"}])


def test_unexpected_request_error_is_clear():
    client = OllamaClient(
        Config(stream=False),
        FakeSession(error=requests.RequestException("bad request")),
    )
    with pytest.raises(OllamaError, match="request failed"):
        client.chat([{"role": "user", "content": "hi"}])


def test_unexpected_stream_request_error_is_clear():
    client = OllamaClient(
        Config(stream=True),
        FakeSession(error=requests.RequestException("bad stream")),
    )
    with pytest.raises(OllamaError, match="request failed"):
        client.chat([{"role": "user", "content": "hi"}], on_chunk=lambda chunk: None)


def test_missing_model_names_the_pull_command():
    response = FakeResponse(status_code=404, text="model not found")
    client = OllamaClient(Config(model="qwen2.5:3b", stream=False), FakeSession(response))
    with pytest.raises(OllamaModelError, match="ollama pull qwen2.5:3b"):
        client.chat([{"role": "user", "content": "hi"}])


def test_empty_response_is_reported():
    response = FakeResponse(payload={"message": {"content": "   "}})
    client = OllamaClient(Config(stream=False), FakeSession(response))
    with pytest.raises(OllamaResponseError, match="empty response"):
        client.chat([{"role": "user", "content": "hi"}])


def test_list_models_reads_names():
    response = FakeResponse(payload={"models": [{"name": "qwen2.5:3b"}, {"name": "other"}]})
    client = OllamaClient(Config(stream=False), FakeSession(response))
    assert client.list_models() == ("qwen2.5:3b", "other")


def test_status_checks_the_selected_model():
    class RoutedSession(FakeSession):
        def request(self, method, url, **kwargs):
            if url.endswith("/api/tags"):
                return FakeResponse(payload={"models": [{"name": "qwen2.5:3b"}]})
            return FakeResponse(payload={"version": "0.40.13"})

    client = OllamaClient(Config(model="qwen2.5:3b", stream=False), RoutedSession())
    status = client.status()
    assert status.version == "0.40.13"
    assert status.model_installed is True
    assert status.models == ("qwen2.5:3b",)
