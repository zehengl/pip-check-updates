import io
from pathlib import Path
from typing import List, Tuple

import pytest

from pip_check_updates.parser import load_toml

files_directory = Path(__file__) / ".." / "files"
test_tomls = [
    "Pipfile",
]


def toml_path(toml_name: str) -> Path:
    """Return the correct path object for the TOML file"""
    return Path(files_directory / toml_name).resolve()


expected_packages = [("requests", "2.28.0")]
expected_dev_packages = [("black", "23.0.0")]


def repackage(path: Path, deps: List[Tuple[str, str]]):
    """Prepare the data as the function returns it."""
    # Ugly hack but it works.

    if path.name == "pyproject.toml":
        operator = "=="
    elif path.name == "poetry.toml":
        operator = "==^"
    else:
        operator = "^"
    return [
        [path, dep_name, dep_version, operator, "pypi"]
        for dep_name, dep_version in deps
    ]


@pytest.mark.parametrize(
    "file_name, expected",
    [
        (
            "Pipfile",
            repackage(toml_path("Pipfile"), expected_packages + expected_dev_packages),
        ),
        (
            "poetry.toml",
            repackage(
                toml_path("poetry.toml"), expected_packages + expected_dev_packages
            ),
        ),
        (
            "pyproject.toml",
            repackage(toml_path("pyproject.toml"), expected_packages),
        ),
    ],
)
def test_load_dependencies(file_name, expected):
    deps = []
    path = toml_path(file_name)
    with io.open(path, mode="r", encoding="utf8") as f:
        load_toml(deps, f, path, path.name != "Pipfile")

    assert deps == expected
