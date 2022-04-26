import pytest

from pip_check_updates.args import get_args


@pytest.mark.parametrize(
    "cmd, expected",
    [
        (
            "dev-requirements.txt",
            [
                ("path", "dev-requirements.txt"),
            ],
        ),
        (
            "-u",
            [
                ("upgrade", True),
                ("path", "requirements.txt"),
            ],
        ),
        (
            "--upgrade",
            [
                ("upgrade", True),
                ("path", "requirements.txt"),
            ],
        ),
        (
            "-i",
            [
                ("interactive", True),
                ("path", "requirements.txt"),
            ],
        ),
        (
            "--interactive",
            [
                ("interactive", True),
                ("path", "requirements.txt"),
            ],
        ),
        (
            "--no_ssl_verify",
            [
                ("no_ssl_verify", True),
            ],
        ),
        (
            "--no_recursive",
            [
                ("no_recursive", True),
            ],
        ),
        (
            "--ignore_warning",
            [
                ("ignore_warning", True),
            ],
        ),
        (
            "--show_full_path",
            [
                ("show_full_path", True),
            ],
        ),
        (
            "--no_color",
            [
                ("no_color", True),
            ],
        ),
        (
            "--ignore_additional_labels",
            [
                ("ignore_additional_labels", True),
            ],
        ),
    ],
)
def test_get_args(mocker, cmd, expected):
    mocker.patch("sys.argv", ["pcu", cmd])
    args = get_args()

    for attr, val in expected:
        assert getattr(args, attr) == val
