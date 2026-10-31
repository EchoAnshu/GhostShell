"""Deterministic risk checks for user commands."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import IntEnum


class RiskLevel(IntEnum):
    """Ordered risk levels."""

    LOW = 0
    CAUTION = 1
    HIGH = 2

    @property
    def label(self) -> str:
        return self.name.lower()


@dataclass(frozen=True)
class RiskRule:
    name: str
    pattern: re.Pattern[str]
    level: RiskLevel
    reason: str


@dataclass(frozen=True)
class RiskFinding:
    name: str
    level: RiskLevel
    reason: str


@dataclass(frozen=True)
class RiskReport:
    findings: tuple[RiskFinding, ...] = ()

    @property
    def level(self) -> RiskLevel:
        if not self.findings:
            return RiskLevel.LOW
        return max(finding.level for finding in self.findings)

    @property
    def blocked(self) -> bool:
        return self.level is RiskLevel.HIGH


def _rule(name: str, pattern: str, level: RiskLevel, reason: str) -> RiskRule:
    return RiskRule(name, re.compile(pattern, re.IGNORECASE), level, reason)


RULES: tuple[RiskRule, ...] = (
    _rule(
        "recursive-delete",
        r"\bRemove-Item\b[^\r\n]*-Recurse\b",
        RiskLevel.HIGH,
        "This deletes a folder and everything inside it.",
    ),
    _rule(
        "unix-recursive-delete",
        r"\brm\s+-(?:[a-z]*r[a-z]*f|[a-z]*f[a-z]*r)\b",
        RiskLevel.HIGH,
        "This deletes files and folders recursively with force.",
    ),
    _rule(
        "windows-recursive-delete",
        r"\b(?:del|erase|rd|rmdir)\b[^\r\n]*\/(?:s|q)\b",
        RiskLevel.HIGH,
        "This deletes files or folders in a way that can skip confirmation.",
    ),
    _rule(
        "disk-format",
        r"\b(?:Format-Volume|Clear-Disk|Initialize-Disk)\b|\bformat\s+[a-z]:",
        RiskLevel.HIGH,
        "This can erase or repartition a disk.",
    ),
    _rule(
        "shutdown",
        r"\b(?:shutdown|Restart-Computer|Stop-Computer)\b",
        RiskLevel.HIGH,
        "This can shut down or restart the machine.",
    ),
    _rule(
        "remote-code-execution",
        r"\b(?:Invoke-Expression|iex)\b",
        RiskLevel.HIGH,
        "This can run text as code.",
    ),
    _rule(
        "download-pipe-shell",
        r"\b(?:curl|wget|Invoke-WebRequest|iwr)\b[^\r\n]*\|\s*"
        r"(?:bash|sh|powershell|pwsh|iex|Invoke-Expression)\b",
        RiskLevel.HIGH,
        "This downloads content and sends it to a shell.",
    ),
    _rule(
        "registry-delete",
        r"\breg(?:\.exe)?\s+delete\b",
        RiskLevel.HIGH,
        "This deletes registry keys or values.",
    ),
    _rule(
        "security-disable",
        r"\b(?:Set-MpPreference|Add-MpPreference)\b[^\r\n]*\bDisable",
        RiskLevel.HIGH,
        "This can turn off a security feature.",
    ),
    _rule(
        "privilege-escalation",
        r"\b(?:runas|Start-Process\b[^\r\n]*-Verb\s+RunAs)\b",
        RiskLevel.HIGH,
        "This can start a process with higher privileges.",
    ),
    _rule(
        "fork-bomb",
        r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",
        RiskLevel.HIGH,
        "This is a fork bomb.",
    ),
    _rule(
        "git-reset-hard",
        r"\bgit\s+reset\s+--hard\b",
        RiskLevel.CAUTION,
        "This throws away uncommitted changes.",
    ),
    _rule(
        "git-clean",
        r"\bgit\s+clean\b[^\r\n]*-[a-z]*f",
        RiskLevel.CAUTION,
        "This removes untracked files.",
    ),
    _rule(
        "git-force-push",
        r"\bgit\s+push\b[^\r\n]*(?:--force|-f)\b",
        RiskLevel.CAUTION,
        "This can overwrite remote history.",
    ),
    _rule(
        "force-stop",
        r"\bStop-Process\b[^\r\n]*-Force\b",
        RiskLevel.CAUTION,
        "This stops a process without asking it to close.",
    ),
    _rule(
        "permissions",
        r"\b(?:icacls|takeown|Set-Acl)\b",
        RiskLevel.CAUTION,
        "This changes file or folder permissions.",
    ),
    _rule(
        "package-install",
        r"\b(?:winget|choco|scoop)\s+install\b|\bpip3?\s+install\b|"
        r"\b(?:npm|yarn|pnpm)\s+(?:install|add)\b[^\r\n]*(?:-g|--global)\b",
        RiskLevel.CAUTION,
        "This installs software on the machine.",
    ),
    _rule(
        "execution-policy",
        r"\bSet-ExecutionPolicy\b",
        RiskLevel.CAUTION,
        "This changes which scripts PowerShell will run.",
    ),
    _rule(
        "account-change",
        r"\bnet\s+(?:user|localgroup)\b[^\r\n]*\/(?:add|delete)\b",
        RiskLevel.CAUTION,
        "This changes a local user or group.",
    ),
    _rule(
        "simple-delete",
        r"\bRemove-Item\b(?![^\r\n]*-Recurse\b)",
        RiskLevel.CAUTION,
        "This deletes a file or folder.",
    ),
)


def check_command(command: str) -> RiskReport:
    """Run all deterministic rules against a command."""
    if not command.strip():
        return RiskReport()
    findings = tuple(
        RiskFinding(rule.name, rule.level, rule.reason)
        for rule in RULES
        if rule.pattern.search(command)
    )
    return RiskReport(findings)
