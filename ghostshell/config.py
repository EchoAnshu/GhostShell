"""Configuration loading and validation."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

DEFAULT_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen2.5:3b"
DEFAULT_TIMEOUT = 30.0
DEFAULT_TEMPERATURE = 0.8


class ConfigError(ValueError):
    """Raised when a setting is invalid."""


@dataclass(frozen=True)
class Config:
    """Settings used by one GhostShell session."""

    host: str = DEFAULT_HOST
    model: str = DEFAULT_MODEL
    timeout: float = DEFAULT_TIMEOUT
    temperature: float = DEFAULT_TEMPERATURE
    stream: bool = True
    color: bool = True

    def validate(self) -> Config:
        """Return this config or raise ConfigError."""
        if not self.host.startswith(("http://", "https://")):
            raise ConfigError("GHOSTSHELL_HOST must start with http:// or https://.")
        if not self.model.strip():
            raise ConfigError("The model name cannot be empty.")
        if self.timeout <= 0:
            raise ConfigError("The timeout must be greater than zero.")
        if self.temperature < 0 or self.temperature > 2:
            raise ConfigError("The temperature must be between 0 and 2.")
        return self


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigError(f"{name} must be 1 or 0.")


def load_config(args: object, environ: Mapping[str, str] | None = None) -> Config:
    """Build a Config from defaults, environment variables, and CLI flags."""
    env = os.environ if environ is None else environ

    host = env.get("GHOSTSHELL_HOST", DEFAULT_HOST).strip().rstrip("/")
    model = env.get("GHOSTSHELL_MODEL", DEFAULT_MODEL).strip()
    timeout_raw = env.get("GHOSTSHELL_TIMEOUT", str(DEFAULT_TIMEOUT))
    temperature_raw = env.get("GHOSTSHELL_TEMPERATURE", str(DEFAULT_TEMPERATURE))
    stream = _parse_bool(env.get("GHOSTSHELL_STREAM", "1"), "GHOSTSHELL_STREAM")
    color = "NO_COLOR" not in env

    try:
        timeout = float(timeout_raw)
    except ValueError as exc:
        raise ConfigError("GHOSTSHELL_TIMEOUT must be a number.") from exc

    try:
        temperature = float(temperature_raw)
    except ValueError as exc:
        raise ConfigError("GHOSTSHELL_TEMPERATURE must be a number.") from exc

    arg_host = getattr(args, "host", None)
    arg_model = getattr(args, "model", None)
    arg_timeout = getattr(args, "timeout", None)
    arg_temperature = getattr(args, "temperature", None)
    arg_stream = getattr(args, "stream", None)
    arg_color = getattr(args, "color", None)

    if arg_host is not None:
        host = str(arg_host).strip().rstrip("/")
    if arg_model is not None:
        model = str(arg_model).strip()
    if arg_timeout is not None:
        timeout = float(arg_timeout)
    if arg_temperature is not None:
        temperature = float(arg_temperature)
    if arg_stream is not None:
        stream = bool(arg_stream)
    if arg_color is not None:
        color = bool(arg_color)

    return Config(
        host=host,
        model=model,
        timeout=timeout,
        temperature=temperature,
        stream=stream,
        color=color,
    ).validate()
