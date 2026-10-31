from ghostshell.text import StreamSanitizer, sanitize


def test_ansi_sequences_are_removed():
    assert sanitize("\x1b[31mBoo\x1b[0m") == "Boo"


def test_control_characters_are_removed():
    assert sanitize("Boo\x07\x00 there\x7f") == "Boo there"


def test_code_fences_are_removed():
    assert sanitize("```powershell\nGet-ChildItem\n```") == "Get-ChildItem"


def test_extra_blank_lines_are_collapsed():
    assert sanitize("one\n\n\n\ntwo") == "one\n\ntwo"


def test_long_text_is_shortened():
    text = sanitize("word " * 200, max_chars=30)
    assert text.endswith("...")
    assert len(text) <= 30


def test_stream_holds_a_split_escape_sequence():
    sanitizer = StreamSanitizer()
    assert sanitizer.feed("\x1b[31") == ""
    assert sanitizer.feed("mBoo\x1b[0m") == "Boo"
    assert sanitizer.flush() == ""


def test_stream_preserves_spaces_between_chunks():
    sanitizer = StreamSanitizer()
    assert sanitizer.feed("Boo ") == "Boo "
    assert sanitizer.feed("there") == "there"
    assert sanitizer.flush() == ""


def test_stream_limits_output():
    sanitizer = StreamSanitizer(max_chars=10)
    output = sanitizer.feed("abcdefghijklmnop")
    assert output == "abcdefghij"
    assert sanitizer.flush() == ""
