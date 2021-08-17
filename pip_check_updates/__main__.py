import argparse

import urllib3
from colorama import Fore, Style, init
from tabulate import tabulate
from tqdm import tqdm

from . import compare_versions, get_latest_version, load_dependencies


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
        "-t",
        "--target",
        choices=["latest", "newest", "greatest", "minor", "patch"],
        help="target version to upgrade to: latest, newest, greatest, minor, patch.",
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
    path = args.path
    upgrade = args.upgrade
    target = args.target
    no_ssl_verify = args.no_ssl_verify

    if no_ssl_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    deps = load_dependencies(path)

    action = "Upgrading" if upgrade else "Checking"
    print(f"{action} dependencies")

    results = {}
    for path, name, current_version, op in tqdm(
        deps, bar_format="{l_bar}{bar:20}{r_bar}"
    ):
        latest_version = get_latest_version(name, no_ssl_verify)
        change = compare_versions(current_version, latest_version)

        if not change:
            continue

        if target in ["latest, newest", "greatest"]:
            pass

        if target == "minor":
            if change == "major":
                continue

        if target == "patch":
            if change in ["major", "minor"]:
                continue

        if path not in results:
            results[path] = []

        results[path].append(
            (
                name,
                current_version,
                latest_version,
                change,
                op,
            )
        )

    print()

    if results:
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

            print(tabulate(table, tablefmt="plain"))

            print()

        styled_path = [Fore.BLUE + key + Style.RESET_ALL for key in results.keys()]
        if upgrade:
            print(
                "Run",
                Fore.YELLOW + "pip install -r ..." + Style.RESET_ALL,
                "to install new versions",
            )
        else:
            print(
                "Run",
                Fore.YELLOW + "pcu -u" + Style.RESET_ALL,
                "to upgrade",
                f"{' and '.join(styled_path)}",
            )
    else:
        print(
            "All dependencies match the latest package versions",
            Fore.GREEN + ":)" + Style.RESET_ALL,
        )

    print()

    if upgrade:
        for path in results:
            with open(path) as f:
                content = f.read()
            for name, current_version, latest_version, _, op in results[path]:
                content = content.replace(
                    f"{name}{op}{current_version}",
                    f"{name}{op}{latest_version}",
                )
            with open(path, "w") as f:
                f.write(content)


if __name__ == "__main__":
    run()
