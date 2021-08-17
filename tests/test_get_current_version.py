import pytest

from pip_check_updates import get_current_version


@pytest.mark.parametrize(
    "dep, name, version, op",
    [
        ("a==1.0", "a", "1.0", "=="),
        ("a>=1.0", "a", "1.0", ">="),
        ("a<=1.0", "a", "1.0", "<="),
        ("a>1.0", "a", "1.0", ">"),
        ("a<1.0", "a", "1.0", "<"),
        ("a~=1.0", "a", "1.0", "~="),
        ("a!=1.0", "a", "1.0", "!="),
    ],
)
def test_get_current_version(dep, name, version, op):
    assert get_current_version(dep) == (name, version, op)
