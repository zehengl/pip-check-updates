<div align="center">
    <img src="https://cdn2.iconfinder.com/data/icons/flat-jewels-icon-set/512/0000_Refresh.png" alt="logo" height="196">
</div>

# pip-check-updates

[![pytest](https://github.com/zehengl/pip-check-updates/actions/workflows/pytest.yml/badge.svg)](https://github.com/zehengl/pip-check-updates/actions/workflows/pytest.yml)
![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)
![PyPI - License](https://img.shields.io/pypi/l/pip-check-updates)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pip-check-updates)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pip-check-updates)
[![Downloads](https://pepy.tech/badge/pip-check-updates)](https://pepy.tech/project/pip-check-updates)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

A tool to upgrade dependencies to the latest versions, inspired by [npm-check-updates](https://www.npmjs.com/package/npm-check-updates)

## Install

From [PyPi](https://pypi.org/project/pip-check-updates/)

    pip install pip-check-updates

From [GitHub](https://github.com/zehengl/pip-check-updates)

    pip install git+https://github.com/zehengl/pip-check-updates.git

## Usage

> Depends on where you install `pip-check-updates`, if Python's scripts folder is not in `path`, the `pcu` entry point would not be available.
> However you can replace `pcu` with `python -m pip-check-updates`.

Show any new dependencies for the project in the current directory:

> Changes are color coded

> - Red = major upgrade
> - Cyan = minor upgrade
> - Green = patch upgrade

```terminal
pcu
```

    Checking dependencies
    100%|████████████████████| 6/6 [00:01<00:00,  5.75it/s]

    In requirements.txt

    tqdm    4.62.0  →  4.62.1
    pandas  0.25.3  →  1.3.2
    Django  3.1.13  →  3.2.6

    Run pcu requirements.txt -u to upgrade versions in 1 file

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

    Run pip install -r requirements.txt to install new versions

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

    Run pcu requirements-dev.txt -u to upgrade versions in 2 files

Target version:

```terminal
pcu requirements-dev.txt -t patch
```

    Checking dependencies
    100%|████████████████████| 10/10 [00:02<00:00,  4.73it/s]

    In requirements.txt

    tqdm  4.62.0  →  4.62.1

    In requirements-dev.txt

    pylint  2.9.3  →  2.9.6

    Run pcu requirements-dev.txt -u to upgrade versions in 2 files

Filter by a pattern:

```terminal
pcu requirements-dev.txt -f "py*"
```

    Checking dependencies
    100%|████████████████████| 10/10 [00:01<00:00,  6.01it/s]

    In requirements-dev.txt

    pylint  2.9.3  →  2.9.6
    pytest  5.4.3  →  6.2.4

    Run pcu requirements-dev.txt -u to upgrade versions in 1 file

Work with conda-forge (WIP):

```terminal
pcu environment.yml -u
```

Work with Pipenv (WIP)

```terminal
pcu Pipfile
```

Show the helper text:

```terminal
pcu -h
```

    usage: pcu [-h] [-u] [-f FILTER [FILTER ...]] [-t {latest,newest,greatest,minor,patch}] [-x] [-i] [--no_ssl_verify] [--no_recursive] [--ignore_warning] [--show_full_path] [--no_color] [path]

    pip-check-updates.

    positional arguments:
    path                  specify path to a requirements file

    optional arguments:
    -h, --help            show this help message and exit
    -u, --upgrade         overwrite package file with upgraded versions instead of just outputting to console.
    -f FILTER [FILTER ...], --filter FILTER [FILTER ...]
                            include only package names matching the given strings.
    -t {latest,newest,greatest,minor,patch}, --target {latest,newest,greatest,minor,patch}
                            target version to upgrade to: latest, newest, greatest, minor, patch.
    -x, --txt             output new requirements file instead of human-readable message.
    -i, --interactive     enable interactive prompts for each dependency.
    --no_ssl_verify       disable SSL verification.
    --no_recursive        disable recursive checking.
    --ignore_warning      ignore warning.
    --show_full_path      show full path.
    --no_color            disable color.



## Test

    python setup.py test

## Credits

- [Icon](https://www.iconfinder.com/icons/171269/refresh_icon) by PixelKit

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/ghostebony"><img src="https://avatars.githubusercontent.com/u/47510020?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Pedro Américo</b></sub></a><br /><a href="https://github.com/zehengl/pip-check-updates/issues?q=author%3Aghostebony" title="Bug reports">🐛</a> <a href="https://github.com/zehengl/pip-check-updates/commits?author=ghostebony" title="Code">💻</a></td>
    <td align="center"><a href="http://kodare.net"><img src="https://avatars.githubusercontent.com/u/332428?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Anders Hovmöller</b></sub></a><br /><a href="https://github.com/zehengl/pip-check-updates/issues?q=author%3Aboxed" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://jtiai.github.io/"><img src="https://avatars.githubusercontent.com/u/1370289?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jani Tiainen</b></sub></a><br /><a href="https://github.com/zehengl/pip-check-updates/issues?q=author%3Ajtiai" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://pelsmaeker.net/"><img src="https://avatars.githubusercontent.com/u/647530?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Daniel A.A. Pelsmaeker</b></sub></a><br /><a href="https://github.com/zehengl/pip-check-updates/issues?q=author%3AVirtlink" title="Bug reports">🐛</a></td>
    <td align="center"><a href="https://github.com/nikolaik"><img src="https://avatars.githubusercontent.com/u/104154?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Nikolai Røed Kristiansen</b></sub></a><br /><a href="#ideas-nikolaik" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
