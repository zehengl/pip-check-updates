import itertools
import re
from pathlib import Path

import requests
import toml
import yaml
from bs4 import BeautifulSoup


def get_latest_version(name, source, no_ssl_verify):
    if source == "pypi":
        r = requests.get(f"https://pypi.org/pypi/{name}/json", verify=not no_ssl_verify)
        if r.status_code == 200:
            version = r.json()["info"]["version"]
            return version
    elif source == "conda":
        r = requests.get(
            f"https://anaconda.org/conda-forge/{name}", verify=not no_ssl_verify
        )
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, "html.parser")
            smalls = soup.find_all("small", {"class": "subheader"})
            if smalls:
                version = smalls[0].text
            else:
                version = None
            return version
    return None


def get_current_version(dep):
    name, current_version = [token for token in re.split(r"[><=~!]", dep) if token]
    op = dep[len(name) : -len(current_version)]
    return name, current_version, op


def compare_versions(current_version, latest_version):
    current_versioning = current_version.split(".")
    latest_versioning = latest_version.split(".")

    max_size = max(len(current_versioning), len(latest_versioning))
    if max_size < 3:
        max_size = 3

    current_versioning = current_versioning + ["0"] * (
        max_size - len(current_versioning)
    )
    latest_versioning = latest_versioning + ["0"] * (max_size - len(latest_versioning))

    if latest_versioning == current_versioning:
        return None

    if latest_versioning[0] != current_versioning[0]:
        return "major"

    if latest_versioning[1] != current_versioning[1]:
        return "minor"

    if latest_versioning[2] != current_versioning[2]:
        return "patch"

    return "other"


def load_txt(deps, f, p, recursive):
    for dep in f.read().splitlines():
        dep = re.sub(r"#.*", "", dep).strip()
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
    config = yaml.safe_load(f)
    dependencies = config.get("dependencies", [])
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
                deps.append([p, name, current_version, op, source])
            except:
                pass


def load_toml(deps, f, p):
    config = toml.load(f)
    packages = list(config.get("packages", {}).items())
    dev_packages = list(config.get("dev-packages", {}).items())
    dependencies = packages + dev_packages
    results = []
    for key, val in dependencies:
        if type(val) is str:
            if val == "*":
                continue
            results.append(f"{key}{val}")
        elif "version" in val:
            if val["version"] == "*":
                continue
            results.append(f"{key}{val['version']}")

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
        else:
            raise RuntimeError(f"Unknown file: {p.name}")

    deps = list(dep for dep, _ in itertools.groupby(deps))

    return deps
