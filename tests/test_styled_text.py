import pytest

from pip_check_updates.style import styled_text


@pytest.mark.parametrize(
    "text, category, no_color",
    [
        ("text", "major", True),
        ("text", "minor", True),
        ("text", "patch", True),
        ("text", "other", True),
        ("text", "cmd", True),
        ("text", "warning", True),
        ("text", "success", True),
        ("text", "xxx", True),
        ("text", "major", False),
        ("text", "minor", False),
        ("text", "patch", False),
        ("text", "other", False),
        ("text", "cmd", False),
        ("text", "warning", False),
        ("text", "success", False),
        ("text", "xxx", False),
    ],
)
def test_styled_text(text, category, no_color):
    if no_color:
        assert text == styled_text(text, category, no_color)
    else:
        assert text in styled_text(text, category, no_color)
