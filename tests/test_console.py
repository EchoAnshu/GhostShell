from io import StringIO

from ghostshell.console import Console


def test_banner_warns_that_the_model_can_be_wrong():
    stream = StringIO()
    console = Console(color=False, stream=stream)
    console.banner()
    output = stream.getvalue()
    assert "GhostShell" in output
    assert "can be wrong" in output
    assert "/help" in output


def test_color_is_disabled_for_a_non_terminal_stream():
    stream = StringIO()
    console = Console(color=True, stream=stream)
    console.warning("careful")
    assert console.color is False
    assert stream.getvalue() == "careful\n"
