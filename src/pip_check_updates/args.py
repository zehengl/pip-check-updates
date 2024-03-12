import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description="pip-check-updates: A tool to upgrade dependencies to the latest versions, inspired by npm-check-updates."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="specify path to a requirements file",
    )
    parser.add_argument(
        "-u",
        "--upgrade",
        action="store_true",
        default=None,
        help="overwrite package file with upgraded versions instead of just outputting to console.",
    )
    parser.add_argument(
        "-f",
        "--filter",
        nargs="+",
        default=None,
        help="include only package names matching the given strings.",
    )
    parser.add_argument(
        "-t",
        "--target",
        choices=["latest", "newest", "greatest", "major", "minor", "patch"],
        default=None,
        help="target version to upgrade to: latest, newest, greatest, major, minor, patch.",
    )
    parser.add_argument(
        "-x",
        "--txt",
        action="store_true",
        default=None,
        help="output new requirements file instead of human-readable message.",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        default=None,
        help="enable interactive prompts for each dependency.",
    )
    parser.add_argument(
        "--no_ssl_verify",
        action="store_true",
        default=None,
        help="disable SSL verification.",
    )
    parser.add_argument(
        "--no_recursive",
        action="store_true",
        default=None,
        help="disable recursive checking.",
    )
    parser.add_argument(
        "--ignore_warning",
        action="store_true",
        default=None,
        help="ignore warning.",
    )
    parser.add_argument(
        "--show_full_path",
        action="store_true",
        default=None,
        help="show full path.",
    )
    parser.add_argument(
        "--no_color",
        action="store_true",
        default=None,
        help="disable color.",
    )
    parser.add_argument(
        "--ignore_additional_labels",
        action="store_true",
        default=None,
        help="ignore additional labels.",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        default=None,
        help="initialize pcufile.toml.",
    )
    parser.add_argument(
        "--extra",
        action="append",
        type=str,
        default=None,
        help="extras to consider when parsing TOML files. Not used with Pipfile.",
    )
    parser.add_argument(
        "--pre",
        action="store_true",
        default=False,
        help="include unstable versions when checking for updates.",
    )
    parser.add_argument(
        "--fail_on_update",
        action="store_true",
        help="exit with code 1 if updates are available.",
    )
    parser.add_argument(
        "--loggable",
        action="store_true",
        help="to be logging friendly.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="show pip-check-updates version",
    )

    args, unknown = parser.parse_known_args()

    return args, unknown
