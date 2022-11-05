"""Module including all the functions for parsing the input files"""
import itertools
import re
from pathlib import Path

import toml
import yaml

from .exceptions import FormatNotSupportedError
from .version import get_current_version


def load_txt(deps, f, p, recursive):
    """
    https://pip.pypa.io/en/stable/reference/requirements-file-format/
    https://pip.pypa.io/en/stable/cli/pip_install/#requirement-specifiers
    """
    content = f.read()
    content = re.sub(r"\\\n", "", content)
    for dep in content.splitlines():
        dep = re.sub(r"#.*", "", dep).strip()
        dep = re.sub(r";.*", "", dep).strip()
        dep = re.sub(r"{%.*?%}", "", dep).strip()
        dep = re.sub(r"{{.*?}}", "", dep).strip()
        if not dep:
            continue
        if dep.startswith("-r") and recursive:
            deps.extend(
                load_dependencies(
                    p.parent / dep.partition("-r")[-1].strip(),
                    recursive,
                )
            )
            continue
        if dep.startswith("-f"):
            continue
        try:
            name, current_version, op = get_current_version(dep)
            deps.append([p, name, current_version, op, "pypi"])
        except:
            pass


def load_yaml(deps, f, p):
    content = f.read()
    content = re.sub(r"\\\n", "", content)
    rows = []
    for row in content.splitlines():
        if not re.search(r"{%.*?%}", row) and not re.search(r"{{.*?}}", row):
            rows.append(row)
    config = yaml.safe_load("\n".join(rows))
    dependencies = config.get("dependencies", [])
    channels = config.get("channels", ["conda-forge"])
    results = {
        "pypi": [],
        "conda": [],
    }
    for val in dependencies:
        if type(val) is str:
            results["conda"].append(val)
        if type(val) is dict:
            results["pypi"].extend(val.get("pip", []))
    for source in results:
        for dep in results[source]:
            try:
                name, current_version, op = get_current_version(dep)
                if source == "conda":
                    source = channels
                deps.append([p, name, current_version, op, source])
            except:
                pass


def load_toml(deps, f, p, poetry=False):
    config = toml.load(f)
    if poetry:
        config = config.get("tool", {}).get("poetry", {})
    separator = "==" if poetry else ""
    package_key = "dependencies" if poetry else "packages"
    packages = list(config.get(package_key, {}).items())
    dev_packages = list(config.get(f"dev-{package_key}", {}).items())
    dependencies = packages + dev_packages

    results = []
    for key, val in dependencies:
        if poetry and key == "python":
            # poetry requires a mandatory python version, which is not a valid pip package.
            # https://python-poetry.org/docs/pyproject/#dependencies-and-dev-dependencies
            continue
        if type(val) is str:
            if val == "*":
                continue
            results.append(f"{key}{separator}{val}")
        elif "version" in val:
            if val["version"] == "*":
                continue
            results.append(f"{key}{separator}{val['version']}")

    for dep in results:
        try:
            name, current_version, op = get_current_version(dep)
            deps.append([p, name, current_version, op, "pypi"])
        except:
            pass


def load_dependencies(path="requirements.txt", recursive=True):
    p = Path(path).resolve()
    deps = []
    with open(p) as f:
        if p.suffix == ".txt":
            load_txt(deps, f, p, recursive)
        elif p.suffix in [".yml", ".yaml"]:
            load_yaml(deps, f, p)
        elif p.name == "Pipfile":
            load_toml(deps, f, p)
        elif p.name == "pyproject.toml":
            load_toml(deps, f, p, poetry=True)
        else:
            raise FormatNotSupportedError

    deps = list(dep for dep, _ in itertools.groupby(deps))

    return deps
