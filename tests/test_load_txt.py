import io
from pathlib import Path

import pytest

from pip_check_updates.parser import load_txt

txt_basic = r"""
black==22.3.0
pylint>=2.13.0
pytest==7.1.*""".strip()

txt_markers_hashes = r"""
django==3.2.13; python_version >= "3.6" \
--hash=sha256:b896ca61edc079eb6bbaa15cf6071eb69d6aac08cce5211583cfb41515644fdf \
--hash=sha256:6d93497a0a9bf6ba0e0b1a29cccdc40efbfc76297255b1309b3a884a688ec4b6
""".strip()

p = Path("requirements.txt").resolve()


@pytest.mark.parametrize(
    "txt, expected",
    [
        (
            txt_basic,
            [
                [p, "black", "22.3.0", "==", "pypi"],
                [p, "pylint", "2.13.0", ">=", "pypi"],
                [p, "pytest", "7.1.*", "==", "pypi"],
            ],
        ),
        (txt_markers_hashes, [[p, "django", "3.2.13", "==", "pypi"]]),
    ],
)
def test_load_txt(txt, expected):
    deps = []
    with io.StringIO(txt) as f:
        load_txt(deps, f, p, True)

    assert deps == expected
