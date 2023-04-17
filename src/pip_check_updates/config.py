from pathlib import Path

import toml

template = {
    "target": "latest",
    "no_ssl_verify": False,
    "ignore_warning": False,
    "show_full_path": False,
    "upgrade": False,
    "no_color": False,
    "no_recursive": False,
    "ignore_additional_labels": False,
    "filter": [],
    "ignores": [],
    "default_venv": ".venv",
    "interactive": False,
    "txt": False,
    "init": False,
    "path": "requirements.txt",
    "extra": [],
    "pre": False,
}

name = "pcufile.toml"


def read():
    if not Path(name).exists():
        return {}

    with open(name) as f:
        return toml.load(f)


def init_config():
    if Path(name).exists():
        with open(name) as f:
            config = toml.load(f)
        for key in template:
            if key not in config:
                config[key] = template[key]
        with open(name, "w") as f:
            toml.dump(config, f)
        return

    with open(name, "w") as f:
        toml.dump(template, f)
