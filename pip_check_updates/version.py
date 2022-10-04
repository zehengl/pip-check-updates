"""Module responsible for version parsing."""
import re

import requests
from bs4 import BeautifulSoup


def get_latest_version(name, source, no_ssl_verify):
    if source == "pypi":
        r = requests.get(f"https://pypi.org/pypi/{name}/json", verify=not no_ssl_verify)
        if r.status_code == 200:
            version = r.json()["info"]["version"]
            return version
    elif type(source) is list:
        version = None
        for channel in source:
            r = requests.get(
                f"https://anaconda.org/{channel}/{name}", verify=not no_ssl_verify
            )
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html.parser")
                smalls = soup.find_all("small", {"class": "subheader"})
                if smalls:
                    version = smalls[0].text
                    break
        return version
    return None


def get_current_version(dep):
    name, current_version = [token for token in re.split(r"[><=~!^]", dep) if token]
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

    if current_versioning[1] == "*":
        return None

    if latest_versioning[1] != current_versioning[1]:
        return "minor"

    if current_versioning[2] == "*":
        return None

    if latest_versioning[2] != current_versioning[2]:
        return "patch"

    return "other"
