import pytest

from pip_check_updates.filter import is_a_match


@pytest.mark.parametrize(
    "pattern, name, expected",
    [
        ("a", "a", True),
        ("a", "b", False),
        ("a*", "abc", True),
        ("a*", "ab", True),
        ("a?", "abc", False),
        ("a?", "ab", True),
        ("a[abc]", "aa", True),
        ("a[abc]", "ab", True),
        ("a[abc]", "ac", True),
        ("a[abc]", "ad", False),
        ("a[abc]", "aaa", False),
        ("a[abc]", "abb", False),
        ("a[abc]", "acc", False),
        ("a[abc]", "add", False),
        ("a[!abc]", "aa", False),
        ("a[!abc]", "ab", False),
        ("a[!abc]", "ac", False),
        ("a[!abc]", "ad", True),
    ],
)
def test_is_a_match(pattern, name, expected):
    assert expected == is_a_match(pattern, name)
