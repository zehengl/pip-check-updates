<figure markdown>
![Logo](https://cdn2.iconfinder.com/data/icons/flat-jewels-icon-set/512/0000_Refresh.png){ width="100" }
</figure>

# pip-check-updates

A tool to upgrade dependencies to the latest versions, inspired by [npm-check-updates](https://www.npmjs.com/package/npm-check-updates)

## Install

    pip install pip-check-updates

## Usage

### Minimal

    pcu

Show all updates of libraries specified in the default `requirements.txt` file.

```{ .text .no-copy }
Checking dependencies
100%|████████████████████| 6/6 [00:01<00:00,  5.75it/s]

In requirements.txt

Django  3.1.13  →  3.2.6
pandas  0.25.3  →  1.3.2
tqdm    4.62.0  →  4.62.1

Run pcu requirements.txt -u to upgrade versions in 1 file
```

### Custom File

    pcu requirements-dev.txt

Specify a requirements file if needed, `-r` option will be recognized as well.

```{ .text .no-copy }
Checking dependencies
100%|████████████████████| 10/10 [00:01<00:00,  6.05it/s]

In requirements.txt

Django  3.1.13  →  3.2.6
pandas  0.25.3  →  1.3.2
tqdm    4.62.0  →  4.62.1

In requirements-dev.txt

black   21.6b0  →  21.7b0
pylint  2.9.3   →  2.9.6
pytest  5.4.3   →  6.2.4

Run pcu requirements-dev.txt -u to upgrade versions in 2 files
```

### Upgrade

    pcu -u

Overwrite the `requirements.txt` file

```{ .text .no-copy }
Upgrading dependencies
100%|████████████████████| 6/6 [00:01<00:00,  5.84it/s]

In requirements.txt

Django  3.1.13  →  3.2.6
pandas  0.25.3  →  1.3.2
tqdm    4.62.0  →  4.62.1

Run pip install -r requirements.txt to install new versions
```

### More

    pcu -h

```{ .text .no-copy }
usage: pcu [-h] [-u] [-f FILTER [FILTER ...]] [-t {latest,newest,greatest,major,minor,patch}] [-x] [-i] [--no_ssl_verify] [--no_recursive] [--ignore_warning] [--show_full_path]
        [--no_color] [--ignore_additional_labels] [--init] [--extra EXTRA] [--pre] [--fail_on_update] [--loggable]
        [path]

pip-check-updates: A tool to upgrade dependencies to the latest versions, inspired by npm-check-updates.

positional arguments:
path                  specify path to a requirements file

optional arguments:
-h, --help            show this help message and exit
-u, --upgrade         overwrite package file with upgraded versions instead of just outputting to console.
-f FILTER [FILTER ...], --filter FILTER [FILTER ...]
                        include only package names matching the given strings.
-t {latest,newest,greatest,major,minor,patch}, --target {latest,newest,greatest,major,minor,patch}
                        target version to upgrade to: latest, newest, greatest, major, minor, patch.
-x, --txt             output new requirements file instead of human-readable message.
-i, --interactive     enable interactive prompts for each dependency.
--no_ssl_verify       disable SSL verification.
--no_recursive        disable recursive checking.
--ignore_warning      ignore warning.
--show_full_path      show full path.
--no_color            disable color.
--ignore_additional_labels
                        ignore additional labels.
--init                initialize pcufile.toml.
--extra EXTRA         extras to consider when parsing TOML files. Not used with Pipfile.
--pre                 include unstable versions when checking for updates.
--fail_on_update      exit with code 1 if updates are available.
--loggable            to be logging friendly.
```
