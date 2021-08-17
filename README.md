<div align="center">
    <img src="https://cdn2.iconfinder.com/data/icons/flat-jewels-icon-set/512/0000_Refresh.png" alt="logo" height="196">
</div>

# pip-check-updates

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)

A tool to upgrade dependencies to the latest versions, inspired by [npm-check-updates](https://www.npmjs.com/package/npm-check-updates)

## Install

From [PyPi](https://pypi.org/project/pip-check-updates/)

    pip install pip-check-updates

From [GitHub](https://github.com/zehengl/pip-check-updates)

    pip install git+https://github.com/zehengl/pip-check-updates.git

## Usage

Show any new dependencies for the project in the current directory:

- Red = major upgrade
- Cyan = minor upgrade
- Green = patch upgrade

```terminal
pcu
```

    Checking dependencies
    100%|████████████████████| 6/6 [00:01<00:00,  5.75it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    Run pcu -u to upgrade requirements.txt

Upgrade a project's requirements file:

```terminal
pcu -u
```

    Upgrading dependencies
    100%|████████████████████| 6/6 [00:01<00:00,  5.84it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    Run pip install -r ... to install new versions

Specify requirements file if needed, `-r` option will be recognized as well:

```terminal
pcu requirements-dev.txt
```

    Checking dependencies
    100%|████████████████████| 10/10 [00:01<00:00,  6.05it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    In requirements-dev.txt

    black   21.6b0  →  21.7b0
    pylint  2.9.3   →  2.9.6
    pytest  5.4.3   →  6.2.4

    Run pcu -u to upgrade requirements.txt and requirements-dev.txt

Show the helper text:

```terminal
pcu -h
```

    usage: pcu [-h] [-u] [-t {latest,newest,greatest,minor,patch}] [path]

    pip-check-updates.

    positional arguments:
    path                  specify path to a requirements file

    optional arguments:
    -h, --help            show this help message and exit
    -u, --upgrade         overwrite package file with upgraded versions instead of just outputting to console.
    -t {latest,newest,greatest,minor,patch}, --target {latest,newest,greatest,minor,patch}
                            target version to upgrade to: latest, newest, greatest, minor, patch.

## Test

    python setup.py test

## Credits

- [Icon](https://www.iconfinder.com/icons/171269/refresh_icon) by PixelKit
