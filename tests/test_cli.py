from io import StringIO

from ghostshell.cli import main, run_cli
from ghostshell.config import Config
from ghostshell.console import Console
from ghostshell.ollama import OllamaConnectionError, OllamaStatus


class FakeClient:
    def __init__(self, text="The repo is restless.", error=None, status=None):
        self.text = text
        self.error = error
        self.status_value = status
        self.calls = []

    def chat(self, messages, on_chunk=None):
        self.calls.append(messages)
        if self.error is not None:
            raise self.error
        if on_chunk is not None:
            on_chunk(self.text)
        return self.text

    def status(self):
        if self.status_value is None:
            return OllamaStatus("0.40.13", ("qwen2.5:3b",), True)
        return self.status_value


class FakeTerminal:
    def __init__(self, lines, answers=()):
        self.lines = iter(lines)
        self.answers = iter(answers)
        self.runs = []
        self.questions = []

    def read(self, prompt):
        try:
            return next(self.lines)
        except StopIteration as exc:
            raise EOFError from exc

    def confirm(self, question, default=False):
        self.questions.append(question)
        try:
            return next(self.answers)
        except StopIteration:
            return False

    def run(self, command, timeout=120):
        self.runs.append(command)
        return 0


def make_config(**values):
    defaults = {"stream": True, "color": False}
    defaults.update(values)
    return Config(**defaults)


def run(lines, answers=(), client=None, config=None):
    output = StringIO()
    console = Console(color=False, stream=output)
    fake_client = client if client is not None else FakeClient()
    terminal = FakeTerminal(lines, answers)
    code = run_cli(config or make_config(), console, fake_client, terminal)
    return code, output.getvalue(), fake_client, terminal


def test_comment_mode_asks_before_running():
    code, output, client, terminal = run(["git status"], [False])
    assert code == 0
    assert "THE GHOST WHISPERS" in output
    assert "The repo is restless." in output
    assert terminal.runs == []
    assert "Nothing was run." in output
    assert len(client.calls) == 1


def test_comment_mode_runs_only_after_yes():
    code, output, client, terminal = run(["git status"], [True])
    assert code == 0
    assert terminal.runs == ["git status"]
    assert "The repo is restless." in output


def test_explain_mode_never_runs_the_command():
    code, output, client, terminal = run(["explain git log --oneline"])
    assert code == 0
    assert "THE GHOST EXPLAINS" in output
    assert terminal.runs == []
    assert "beginner" in client.calls[0][0]["content"]


def test_high_risk_command_is_blocked_before_the_model():
    code, output, client, terminal = run(["Remove-Item -Recurse .\\build"])
    assert code == 0
    assert "BLOCKED" in output
    assert "GhostShell will not run this command." in output
    assert client.calls == []
    assert terminal.runs == []


def test_caution_command_warns_then_asks():
    code, output, client, terminal = run(["Remove-Item .\\old.txt"], [True])
    assert code == 0
    assert "WARNING" in output
    assert terminal.runs == ["Remove-Item .\\old.txt"]


def test_model_failure_still_offers_to_run_the_command():
    client = FakeClient(error=OllamaConnectionError("Ollama is not running."))
    code, output, client, terminal = run(["git status"], [True], client=client)
    assert code == 0
    assert "Ollama is not running." in output
    assert "Run it without a ghost comment?" in terminal.questions
    assert terminal.runs == ["git status"]


def test_check_reports_the_model():
    code, output, client, terminal = run(["/check"])
    assert code == 0
    assert "Ollama: 0.40.13" in output
    assert "Model status: installed" in output
    assert client.calls == []


def test_help_and_exit():
    code, output, client, terminal = run(["/help", "/exit"])
    assert code == 0
    assert "GHOSTSHELL HELP" in output
    assert "The ghost fades." in output


def test_model_text_is_sanitized_before_printing():
    client = FakeClient(text="\x1b[31mBoo\x1b[0m")
    code, output, client, terminal = run(["git status"], [False], client=client)
    assert code == 0
    assert "Boo" in output
    assert "\x1b" not in output


def test_version_flag(capsys):
    assert main(["--version"]) == 0
    assert "GhostShell 0.1.0" in capsys.readouterr().out


def test_invalid_setting_returns_two(capsys):
    assert main(["--host", "localhost"]) == 2
    assert "must start with" in capsys.readouterr().err
