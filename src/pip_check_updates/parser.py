"""Module including all the functions for parsing the input files"""

import itertools
import re
from pathlib import Path

import toml
import yaml

from .exceptions import FormatNotSupportedError
from .version import get_current_version


def clean_requirements_line(dep):
    """Remove "unsupported" stuff from the requirements line we are parsing."""
    dep = re.sub(r"#.*", "", dep).strip()
    dep = re.sub(r";.*", "", dep).strip()
    dep = re.sub(r"{%.*?%}", "", dep).strip()
    dep = re.sub(r"{{.*?}}", "", dep).strip()
    return dep


def load_txt(deps, f, p, recursive):
    """
    https://pip.pypa.io/en/stable/reference/requirements-file-format/
    https://pip.pypa.io/en/stable/cli/pip_install/#requirement-specifiers
    """
    content = f.read()
    content = re.sub(r"\\\n", "", content)
    for dep in content.splitlines():
        dep = clean_requirements_line(dep)
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


"""TOML has a few different flavors and they each get a different parser."""


def _get_toml_results(dependencies, separator, pyproject=False):
    results = []
    for key, val in dependencies:
        if pyproject and key == "python":
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
    return results


def _set_toml_deps(p, deps, results):
    for dep in results:
        try:
            name, current_version, op = get_current_version(dep)
            deps.append([p, name, current_version, op, "pypi"])
        except:
            pass


def _parse_requirements_lines(requirements_lines):
    """Shared function for properly parsing requirement lines."""
    requirements = [
        get_current_version(clean_requirements_line(requirement_line))
        for requirement_line in requirements_lines
    ]
    deps = [(name, version) for name, version, _ in requirements]
    return deps


def _load_pipfile(p, deps, config):
    """Parse a Pipfile."""
    separator = ""
    package_key = "packages"
    packages = list(config.get(package_key, {}).items())
    dev_packages = list(config.get(f"dev-{package_key}", {}).items())
    dependencies = packages + dev_packages
    results = _get_toml_results(dependencies, separator)
    _set_toml_deps(p, deps, results)


def _load_pdm(p, deps, config, extras):
    """Parse a PDM pyproject.toml."""
    project_config = config.get("project", {})
    separator = "=="
    package_key = "dependencies"

    packages = _parse_requirements_lines(project_config.get(package_key, []))
    dev_packages = _parse_requirements_lines(
        config.get("tool", {}).get("pdm", {}).get("dev-dependencies", {}).get("dev", [])
    )
    dependencies = packages + dev_packages

    # Parse extras
    extras_section = "optional-dependencies"
    for extra in extras:
        dependencies += _parse_requirements_lines(
            project_config.get(extras_section, {}).get(extra, [])
        )

    results = _get_toml_results(dependencies, separator, pyproject=True)
    _set_toml_deps(p, deps, results)


def _load_poetry(p, deps, config, extras):
    """Parse a poetry pyproject.toml."""
    config = config.get("tool", {}).get("poetry", {})
    separator = "=="
    package_key = "dependencies"

    packages = list(config.get(package_key, {}).items())
    dev_packages = list(
        config.get("group", {}).get("dev", {}).get(package_key, {}).items()
    )
    dependencies = packages + dev_packages

    # Parse extras
    extras_section = "extras"
    for extra in extras:
        dependencies += _parse_requirements_lines(
            config.get(extras_section, {}).get(extra, [])
        )

    results = _get_toml_results(dependencies, separator, pyproject=True)
    _set_toml_deps(p, deps, results)


def _load_setuptools_and_flit(p, deps, config, extras):
    """Parse a setuptools or flit pyproject.toml."""
    config = config.get("project", {})
    separator = "=="
    package_key = "dependencies"

    # setuptools and flit have a requirements.txt like format.
    # Parse the line and recombine it back in the appropriate way.
    packages = _parse_requirements_lines(config.get(package_key, []))

    # Only Pipfile and poetry support dev dependencies, there is no standard for setuptools and flit
    dependencies = packages

    # Parse extras
    extras_section = "optional-dependencies"
    for extra in extras:
        dependencies += _parse_requirements_lines(
            config.get(extras_section, {}).get(extra, [])
        )

    results = _get_toml_results(dependencies, separator, pyproject=True)
    _set_toml_deps(p, deps, results)


def load_toml(deps, f, p, pyproject=False, extras=[]):
    """Parse a Pipfile or pyproject.toml. By default parses Pipfile."""
    config = toml.load(f)

    is_poetry = "poetry" in config.get("tool", {})
    is_pdm = "pdm" in config.get("tool", {})

    if pyproject:
        # Special handling for pyproject.toml projects which can use
        # different tools
        if is_poetry:
            _load_poetry(p, deps, config, extras)
        elif is_pdm:
            _load_pdm(p, deps, config, extras)
        else:
            # If it's not poetry, then we assume setuptools or flit
            _load_setuptools_and_flit(p, deps, config, extras)
    else:
        _load_pipfile(p, deps, config)


def load_dependencies(path="requirements.txt", recursive=True, extras: list = []):
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
            load_toml(deps, f, p, pyproject=True, extras=extras)
        else:
            raise FormatNotSupportedError

    deps = list(dep for dep, _ in itertools.groupby(deps))

    return deps
