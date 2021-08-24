import argparse
import fnmatch
import re

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

    args = parser.parse_args()

    return args


def styled_version(latest_version, change):
    mapping = {
        "major": Fore.RED,
        "minor": Fore.CYAN,
        "patch": Fore.GREEN,
        "other": Fore.MAGENTA,
    }

    return mapping[change] + latest_version + Style.RESET_ALL


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

    if upgrade and txt_output:
        print("Oops, cannot specify both -u and -x. Please pick one.")
        return

    if no_ssl_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    deps = load_dependencies(req_path)

    if not txt_output:
        action = "Upgrading" if upgrade else "Checking"
        print(f"{action} dependencies")

    results = {}
    for path, name, current_version, op in tqdm(
        deps, bar_format="{l_bar}{bar:20}{r_bar}", disable=txt_output
    ):
        latest_version = get_latest_version(name, no_ssl_verify)
        change = compare_versions(current_version, latest_version)

        if any(
            [
                not change,
                filter_ and not any([is_a_match(pattern, name) for pattern in filter_]),
                target == "minor" and change == "major",
                target == "patch" and change in ["major", "minor"],
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

    if interactive:
        for path in results:
            for t in results[path]:
                name, current_version, latest_version, change, _ = t
                prompt = (
                    "Do you want to upgrade: "
                    f"{name} {current_version} → "
                    f"{styled_version(latest_version, change)}? "
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
            print("In", Fore.BLUE + path + Style.RESET_ALL)
            print()

            table = []
            for name, current_version, latest_version, change, op in results[path]:
                table.append(
                    (
                        name,
                        current_version,
                        "→",
                        styled_version(latest_version, change),
                    )
                )

            print(tabulate(table, tablefmt="plain", disable_numparse=True))

            print()

        styled_path = [Fore.BLUE + key + Style.RESET_ALL for key in results.keys()]
        if upgrade:
            print(
                "Run",
                Fore.YELLOW + f"pip install -r {req_path}" + Style.RESET_ALL,
                "to install new versions",
            )
        else:
            print(
                "Run",
                Fore.YELLOW + "pcu -u" + Style.RESET_ALL,
                "to upgrade",
                f"{' and '.join(styled_path)}",
            )
    elif not txt_output:
        print()
        print(
            "All dependencies match the latest package versions",
            Fore.GREEN + ":)" + Style.RESET_ALL,
        )

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
            print("For", Fore.BLUE + path + Style.RESET_ALL)
            print()
            print(content.strip())
            print()


if __name__ == "__main__":
    run()
