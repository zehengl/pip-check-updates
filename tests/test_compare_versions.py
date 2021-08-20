import pytest

from pip_check_updates import compare_versions


@pytest.mark.parametrize(
    "current_version, latest_version, change",
    [
        ("1", "4", "major"),
        ("1", "4.5", "major"),
        ("1", "4.5.6", "major"),
        ("1", "1", None),
        ("1", "1.0", None),
        ("1", "1.0.0", None),
        ("1", "1.2", "minor"),
        ("1", "1.2.3", "minor"),
        ("1.2", "4", "major"),
        ("1.2", "4.5", "major"),
        ("1.2", "4.5.6", "major"),
        ("1.2", "1.2", None),
        ("1.2", "1.2.0", None),
        ("1.2", "1.1", "minor"),
        ("1.2", "1.3", "minor"),
        ("1.2", "1.3.4", "minor"),
        ("1.2", "1.2.3", "patch"),
        ("1.2.3", "4", "major"),
        ("1.2.3", "4.5", "major"),
        ("1.2.3", "4.5.6", "major"),
        ("1.2.3", "1", "minor"),
        ("1.2.3", "1.1", "minor"),
        ("1.2.3", "1.2", "patch"),
        ("1.2.3", "1.2.3", None),
        ("1.2.3", "1.2.4", "patch"),
        ("1.2.3", "1.2.3.abc", "other"),
        ("1.2.3.1", "1.2.3.1", None),
        ("1.2.3", "1.2.3.0", None),
        ("1.2.3", "1.2.3.0.0", None),
    ],
)
def test_compare_versions(current_version, latest_version, change):
    assert compare_versions(current_version, latest_version) == change
