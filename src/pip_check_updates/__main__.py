from pathlib import Path

import urllib3
from colorama import init
from tabulate import tabulate
from tqdm import tqdm

from .args import get_args
from .config import init_config, read, template
from .exceptions import FormatNotSupportedError
from .filter import is_a_match
from .parser import load_dependencies
from .style import dot_path, styled_text
from .version import compare_versions, get_latest_version


def run():
    init()

    pcu_config = read()

    args, unknown = get_args()

    def get_val(name):
        return getattr(args, name, None) or pcu_config.get(name, template[name])

    req_path = get_val("path")
    txt_output = get_val("txt")
    interactive = get_val("interactive")
    init_ = get_val("init")

    upgrade = get_val("upgrade")
    target = get_val("target")
    no_ssl_verify = get_val("no_ssl_verify")
    filter_ = get_val("filter")
    no_recursive = get_val("no_recursive")
    ignore_warning = get_val("ignore_warning")
    show_full_path = get_val("show_full_path")
    no_color = get_val("no_color")
    ignore_additional_labels = get_val("ignore_additional_labels")
    extra = get_val("extra")
    pre = get_val("pre")

    if unknown:
        print(
            styled_text(
                f"Ignored unrecognized arguments: {', '.join(unknown)}",
                "warning",
                False,
            )
        )
        print()

    if init_:
        init_config()
        return

    is_txt = req_path.endswith(".txt")
    is_yml = req_path.endswith(".yml") or req_path.endswith(".yaml")
    is_toml = req_path == "Pipfile" or req_path.endswith(".toml")

    if upgrade and txt_output:
        print("Oops, cannot specify both -u and -x. Please pick one.")
        return

    if no_ssl_verify:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        deps = load_dependencies(req_path, not no_recursive, extra)
    except FileNotFoundError:
        msg = styled_text(
            f"{Path(req_path).absolute()} does not exist.",
            "error",
            False,
        )
        print(msg)
        return
    except FormatNotSupportedError:
        msg = styled_text(
            f"{Path(req_path).absolute()} is not supported.",
            "error",
            False,
        )
        print(msg)
        return

    if deps and not txt_output:
        action = "Upgrading" if upgrade else "Checking"
        print(f"{action} dependencies")

    ignores = get_val("ignores")

    results = {}
    errors = {}
    for path, name, current_version, op, source in tqdm(
        deps, bar_format="{l_bar}{bar:20}{r_bar}", disable=txt_output or not deps
    ):
        latest_version = get_latest_version(
            name.partition("[")[0], source, no_ssl_verify, pre
        )
        if latest_version is None:
            if type(source) is list:
                source = ", ".join(source)
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
                target == "patch"
                and change in ["latest", "newest", "greatest", "major", "minor"],
                ignore_additional_labels and change == "other",
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
                default_venv = get_val("default_venv")
                conda_cmd = (
                    f"conda env update --prefix {dot_path(Path(default_venv))} --prune"
                )
                cmd = f"{conda_cmd} --file {req_path}"
                print(
                    "Run",
                    styled_text(cmd, "cmd", no_color),
                    "to install new versions",
                    f"\n(assuming you have a local conda environment named '{default_venv}')",
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
                _path = str(path) if show_full_path else path.name
                print("For", styled_text(_path, "info", no_color))
                print()
                print(content.strip())
                print()

    if not ignore_warning and errors:
        print()
        for source, libs in errors.items():
            libs = ", ".join(libs)
            if source == "pypi":
                source = "PyPI"
            elif ", " in source:
                s = "s" if len(source.split(", ")) > 1 else ""
                source = f"channel{s}: {source}"
            message = f"WARNING: could not find {libs} on {source}."
            print(styled_text(message, "warning", no_color))


if __name__ == "__main__":
    run()
