from types import SimpleNamespace

import pytest

from ghostshell.config import ConfigError, load_config


def args(**values):
    return SimpleNamespace(**values)


def test_defaults():
    config = load_config(args(), {})
    assert config.host == "http://127.0.0.1:11434"
    assert config.model == "qwen2.5:3b"
    assert config.timeout == 30.0
    assert config.temperature == 0.8
    assert config.stream is True
    assert config.color is True


def test_environment_overrides_defaults():
    config = load_config(
        args(),
        {
            "GHOSTSHELL_HOST": "http://localhost:1234/",
            "GHOSTSHELL_MODEL": "qwen2.5:0.5b",
            "GHOSTSHELL_TIMEOUT": "60",
            "GHOSTSHELL_TEMPERATURE": "0.2",
            "GHOSTSHELL_STREAM": "0",
            "NO_COLOR": "1",
        },
    )
    assert config.host == "http://localhost:1234"
    assert config.model == "qwen2.5:0.5b"
    assert config.timeout == 60.0
    assert config.temperature == 0.2
    assert config.stream is False
    assert config.color is False


def test_flags_override_environment():
    config = load_config(
        args(
            host="http://127.0.0.1:9999",
            model="llama3.2:3b",
            timeout=10.0,
            temperature=0.1,
            stream=False,
            color=False,
        ),
        {
            "GHOSTSHELL_HOST": "http://localhost:1234",
            "GHOSTSHELL_MODEL": "qwen2.5:3b",
            "GHOSTSHELL_TIMEOUT": "60",
            "GHOSTSHELL_TEMPERATURE": "1.0",
            "GHOSTSHELL_STREAM": "1",
        },
    )
    assert config.host == "http://127.0.0.1:9999"
    assert config.model == "llama3.2:3b"
    assert config.timeout == 10.0
    assert config.temperature == 0.1
    assert config.stream is False
    assert config.color is False


@pytest.mark.parametrize(
    ("environ", "message"),
    [
        ({"GHOSTSHELL_HOST": "localhost:11434"}, "must start with"),
        ({"GHOSTSHELL_MODEL": "   "}, "cannot be empty"),
        ({"GHOSTSHELL_TIMEOUT": "0"}, "greater than zero"),
        ({"GHOSTSHELL_TIMEOUT": "nope"}, "must be a number"),
        ({"GHOSTSHELL_TEMPERATURE": "3"}, "between 0 and 2"),
        ({"GHOSTSHELL_TEMPERATURE": "hot"}, "must be a number"),
        ({"GHOSTSHELL_STREAM": "maybe"}, "must be 1 or 0"),
    ],
)
def test_invalid_settings(environ, message):
    with pytest.raises(ConfigError, match=message):
        load_config(args(), environ)
