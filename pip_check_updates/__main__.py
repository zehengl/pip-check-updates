import argparse
import fnmatch
import re
from pathlib import Path

import urllib3
from colorama import Fore, Style, init
from tabulate import tabulate
from tqdm import tqdm

from . import compare_versions, get_latest_version, load_dependencies


def is_a_match(pattern, name):
    return re.compile(fnmatch.translate(pattern)).match(name) is not None


def get_args():
    parser = argparse.ArgumentParser(description="pip-check-updates.")
    parser.add_argument(
        "path",
        nargs="?",
        default="requirements.txt",
        help="specify path to a requirements file",
    )
    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        default=False,
        help="overwrite package file with upgraded versions instead of just outputting to console.",
    )
    parser.add_argument(
        "-f",
        "--filter",
        nargs="+",
        help="include only package names matching the given strings.",
    )
    parser.add_argument(
        "-t",
        "--target",
        choices=["latest", "newest", "greatest", "minor", "patch"],
        help="target version to upgrade to: latest, newest, greatest, minor, patch.",
    )
    parser.add_argument(
        "-x",
        "--txt",
        action="store_true",
        default=False,
        help="output new requirements file instead of human-readable message.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        default=False,
        help="enable interactive prompts for each dependency.",
    )
    parser.add_argument(
        "--no_ssl_verify",
        action="store_true",
        default=False,
        help="disable SSL verification.",
    )
    parser.add_argument(
        "--no_recursive",
        action="store_true",
        default=False,
        help="disable recursive checking.",
    )
    parser.add_argument(
        "--ignore_warning",
        action="store_true",
        default=False,
        help="ignore warning.",
    )
    parser.add_argument(
        "--show_full_path",
        action="store_true",
        default=False,
        help="show full path.",
    )
    parser.add_argument(
        "--no_color",
        action="store_true",
        default=False,
        help="disable color.",
    )

    args = parser.parse_args()

    return args


def styled_text(text, category, no_color):
    if no_color:
        return text

    mapping = {
        "major": Fore.RED,
        "minor": Fore.CYAN,
        "patch": Fore.GREEN,
        "other": Fore.MAGENTA,
        "info": Fore.BLUE,
        "cmd": Fore.YELLOW,
        "warning": Fore.YELLOW,
        "success": Fore.GREEN,
    }

    color = mapping.get(category)

    if color:
        return color + text + Style.RESET_ALL

    return text


def run():

    init()

    args = get_args()
    req_path = args.path
    upgrade = args.upgrade
    target = args.target
    no_ssl_verify = args.no_ssl_verify
    filter_ = args.filter
    txt_output = args.txt
    interactive = args.interactive
    no_recursive = args.no_recursive
    ignore_warning = args.ignore_warning
    show_full_path = args.show_full_path
    no_color = args.no_color

    is_txt = req_path.endswith(".txt")
    is_yml = req_path.endswith(".yml") or req_path.endswith(".yaml")
    is_toml = req_path == "Pipfile"

    if upgrade and txt_output:
        print("Oops, cannot specify both -u and -x. Please pick one.")
        return

    if no_ssl_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    deps = load_dependencies(req_path, not no_recursive)

    if deps and not txt_output:
        action = "Upgrading" if upgrade else "Checking"
        print(f"{action} dependencies")

    if Path(".pcuignore").exists():
        with open(".pcuignore") as f:
            ignores = [pattern.strip() for pattern in f.readlines()]
    else:
        ignores = []

    results = {}
    errors = {}
    for path, name, current_version, op, source in tqdm(
        deps, bar_format="{l_bar}{bar:20}{r_bar}", disable=txt_output or not deps
    ):
        latest_version = get_latest_version(
            name.partition("[")[0], source, no_ssl_verify
        )
        if latest_version is None:
            if source not in errors:
                errors[source] = []
            errors[source].append(name)
            continue
        change = compare_versions(current_version, latest_version)

        if any(
            [
                not change,
                filter_ and not any([is_a_match(pattern, name) for pattern in filter_]),
                target == "minor" and change == "major",
                target == "patch" and change in ["major", "minor"],
                any([is_a_match(pattern, name) for pattern in ignores]),
            ]
        ):
            continue

        if path not in results:
            results[path] = []

        results[path].append(
            [
                name,
                current_version,
                latest_version,
                change,
                op,
            ]
        )

    for path in results:
        results[path].sort(key=lambda x: x[0])

    if interactive:
        for path in results:
            for t in results[path]:
                name, current_version, latest_version, change, _ = t
                prompt = (
                    "Do you want to upgrade: "
                    f"{name} {current_version} → "
                    f"{styled_text(latest_version, change, no_color)}? "
                )
                answer = input(prompt)
                t.append(answer.lower() in ["y", "yes"])

        for path in results:
            results[path] = [
                (name, current_version, latest_version, change, op)
                for name, current_version, latest_version, change, op, keep in results[
                    path
                ]
                if keep
            ]
        results = {path: tuple_ for path, tuple_ in results.items() if tuple_}

    if results and not txt_output:
        print()
        for path in results:
            _path = str(path) if show_full_path else path.name
            print("In", styled_text(_path, "info", no_color))
            print()

            table = []
            for name, current_version, latest_version, change, op in results[path]:
                table.append(
                    (
                        name,
                        current_version,
                        "→",
                        styled_text(latest_version, change, no_color),
                    )
                )

            print(tabulate(table, tablefmt="plain", disable_numparse=True))

            print()

        if upgrade:
            if is_txt:
                cmd = f"pip install -r {req_path}"
                print(
                    "Run",
                    styled_text(cmd, "cmd", no_color),
                    "to install new versions",
                )
            elif is_yml:
                conda_cmd = "conda env update --prefix ./venv --prune"
                cmd = f"{conda_cmd} --file {req_path}"
                print(
                    "Run",
                    styled_text(cmd, "cmd", no_color),
                    "to install new versions",
                    "\n(assuming you have a local conda environment named 'venv')",
                )
        else:
            if not is_toml:
                cmd = f"pcu {req_path} -u"
                print(
                    "Run",
                    styled_text(cmd, "cmd", no_color),
                    "to upgrade versions",
                    f"in {len(results)} file{'s' if len(results) > 1 else ''}",
                )

    elif not txt_output:
        print()
        print(
            "All dependencies match the latest package versions",
            styled_text(":)", "success", no_color),
        )

    if not is_toml:
        for path in results:
            with open(path) as f:
                content = f.read()
            for name, current_version, latest_version, _, op in results[path]:
                content = content.replace(
                    f"{name}{op}{current_version}",
                    f"{name}{op}{latest_version}",
                )

            if upgrade:
                with open(path, "w") as f:
                    f.write(content)

            if txt_output:
                print("For", styled_text(path, "info", no_color))
                print()
                print(content.strip())
                print()

    if not ignore_warning and errors:
        print()
        mapping = {
            "pypi": "PyPI",
            "conda": "conda-forge",
        }
        for source, libs in errors.items():
            libs = ", ".join(libs)
            message = f"WARNING: could not find {libs} on {mapping[source]}."
            print(styled_text(message, "warning", no_color))


if __name__ == "__main__":
    run()
