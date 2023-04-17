import pytest

from pip_check_updates.args import get_args


@pytest.mark.parametrize(
    "cmd, expected",
    [
        (
            ["dev-requirements.txt"],
            [
                ("path", "dev-requirements.txt"),
            ],
        ),
        (
            ["-u"],
            [
                ("upgrade", True),
            ],
        ),
        (
            ["--upgrade"],
            [
                ("upgrade", True),
            ],
        ),
        (
            ["-i"],
            [
                ("interactive", True),
            ],
        ),
        (
            ["--interactive"],
            [
                ("interactive", True),
            ],
        ),
        (
            ["--no_ssl_verify"],
            [
                ("no_ssl_verify", True),
                ("no_recursive", None),
            ],
        ),
        (
            ["--no_recursive"],
            [
                ("no_recursive", True),
                ("ignore_warning", None),
            ],
        ),
        (
            ["--ignore_warning"],
            [
                ("ignore_warning", True),
                ("show_full_path", None),
            ],
        ),
        (
            ["--show_full_path"],
            [
                ("show_full_path", True),
                ("no_color", None),
            ],
        ),
        (
            ["--no_color"],
            [
                ("no_color", True),
                ("ignore_additional_labels", None),
            ],
        ),
        (
            ["--ignore_additional_labels"],
            [
                ("ignore_additional_labels", True),
            ],
        ),
        (
            ["--pre"],
            [
                ("pre", True),
            ],
        ),
        (
            ["--not_an_valid_argument", "--no_color"],
            [
                ("not_an_valid_argument", "not valid"),
                ("no_color", True),
            ],
        ),
    ],
)
def test_get_args(mocker, cmd, expected):
    mocker.patch("sys.argv", ["pcu", *cmd])
    args, _ = get_args()

    for attr, val in expected:
        if val == "not valid":
            assert attr not in args
        else:
            assert getattr(args, attr) == val
