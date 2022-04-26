from pathlib import Path

import toml

template = """
target = "latest"
no_ssl_verify = false
ignore_warning = false
show_full_path = false
upgrade = false
no_color = false
ignore_additional_labels = false
filter = [
]
ignores =[
]
""".lstrip()

name = "pcufile.toml"


def read():
    if not Path(name).exists():
        return {}

    with open(name) as f:
        return toml.load(f)


def init_config():
    if Path(name).exists():
        return

    with open(name, "w") as f:
        f.write(template)
