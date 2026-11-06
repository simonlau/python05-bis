# Python pip: Standard Package Manager

> Sources: Real Python (Philipp Acsany); 2024-12-22
> Raw: [Using Python's pip to Manage Your Projects' Dependencies](../../raw/python-programming/2026-11-06-realpython-what-is-pip.md)
> Updated: 2026-11-06

## Overview

`pip` is the standard package manager for Python, used to install and manage libraries that aren’t part of the Python standard library. You use `pip` to manage dependencies and install packages from the Python Package Index (PyPI).

The name **pip** was introduced by Ian Bicking in 2008 as an acronym: **"pip installs packages."**

Python’s installers have included `pip` since versions 3.4 and 2.7.9, for Python 3 and Python 2 respectively. Only `pip` comes bundled in the standard Python installation; alternatives like Conda, Poetry, Pipenv, and uv must be installed separately.

## Finding pip on Your System

The Python installer includes `pip` by default. On some Linux systems (e.g., Ubuntu), `pip` comes in a separate package called `python3-pip` and must be installed with `sudo apt install python3-pip`.

### Verify pip is available

**Windows:**
```powershell
PS> where pip3
```

**Linux + macOS:**
```bash
$ which pip3
```

`pip3` may be found in more than one location when multiple Python versions are installed.

### Running pip as a module

Instead of running system `pip` directly, run it as a Python module to ensure the correct Python version is used:

```bash
$ python -m pip
```

The `-m` switch tells Python to run a module as an executable of the `python` interpreter.

## Using pip in a Virtual Environment

To avoid installing packages into your system Python installation, use `pip` inside a virtual environment. Advantages:

1. Be sure you’re using the **right Python version** for the project
2. Be confident you’re referring to the **correct pip instance**
3. Use a **specific package version** without affecting other projects

### Create and activate a virtual environment

**Windows:**
```powershell
PS> python -m venv venv\
PS> venv\Scripts\activate.bat
(venv) PS> pip3 --version
pip 24.2 from ...\lib\site-packages\pip (python 3.12)
```

**Linux + macOS:**
```bash
$ python -m venv venv/
$ source venv/bin/activate
(venv) $ pip3 --version
pip 24.2 from .../python3.12/site-packages/pip (python 3.12)
```

Once activated, you can use either `pip` or `pip3`. For consistency, use `python -m pip` inside the virtual environment.

## Reinstalling pip When Errors Occur

Common `pip` not found errors:

| Operating System | Error Message |
|---|---|
| Windows | `'pip' is not recognized as an internal or external command, operable program or batch file.` |
| Linux | `bash: pip: command not found` |
| macOS | `zsh: command not found: pip` |

These indicate your system can’t find `pip` in your `PATH` variable.

### Method 1: ensurepip (built into Python 3.4+)

```bash
$ python -m ensurepip --upgrade
```

`ensurepip` doesn’t access the Internet. It installs the `pip` version bundled with your Python installation. For example, Python 3.12 bundles `pip` 24.2. For a newer version, run `ensurepip` first, then update `pip` manually.

### Method 2: get-pip.py script

```bash
$ python get-pip.py
```

Downloads from https://bootstrap.pypa.io/get-pip.py. Installs the latest `pip`, `setuptools`, and `wheel`. Use `--no-setuptools --no-wheel` to install only `pip`.

## Installing Packages With pip

### Install from PyPI

```bash
(venv) $ python -m pip install requests
```

`pip install <package>`:
1. Looks for the latest version of the package
2. Resolves dependencies from package metadata
3. Installs everything in your current environment

Install multiple packages:
```bash
(venv) $ python -m pip install rptree codetiming
```

List installed packages:
```bash
(venv) $ python -m pip list
```

Show package metadata:
```bash
(venv) $ python -m pip show requests
```

The `Requires` field lists packages the package depends on (e.g., `requests` requires `certifi`, `idna`, `charset-normalizer`, `urllib3`).

### Install from a Custom Package Index

By default, `pip` uses PyPI. A custom index must comply with PEP 503 – Simple Repository API.

Use `--index-url` (or `-i` shorthand):
```bash
(venv) $ python -m pip install -i https://test.pypi.org/simple/ rptree
```

For permanent use, set `index-url` in `pip.conf`:
```ini
[global]
index-url = https://test.pypi.org/simple/
```

### Install from Git Repositories

```bash
(venv) $ python -m pip install git+https://github.com/realpython/rptree
```

`pip` also supports Mercurial, Subversion, and Bazaar.

### Install in Editable Mode

For developing your own package:

```bash
$ git clone https://github.com/realpython/rptree
$ cd rptree
$ python -m venv venv/
$ source venv/bin/activate
(venv) $ python -m pip install -e .
```

The `-e` flag (shorthand for `--editable`) creates a link in site-packages to the local project path instead of copying files:
```
~/rptree/venv/lib/python3.12/site-packages/rptree.egg-link
```

## Using Requirements Files

### Pinning Requirements

A `requirements.txt` file specifies precisely which packages and versions should be installed.

Generate with `pip freeze`:
```bash
(venv) $ python -m pip freeze > requirements.txt
```

Example:
```
certifi==x.y.z
charset-normalizer==x.y.z
idna==x.y.z
requests==x.y.z
urllib3==x.y.z
```

Replicate in another system:
```bash
(venv) $ python -m pip install -r requirements.txt
```

### Fine-Tuning Requirements

Use comparison operators for flexibility:

```text
certifi>=x.y.z
charset-normalizer>=x.y.z
idna>=x.y.z
requests>=x.y.z
urllib3>=x.y.z
```

Upgrade packages:
```bash
(venv) $ python -m pip install -U -r requirements.txt
```

Prevent incompatible versions:
```text
requests>=x.y.z, <3.0
```

### Separating Production and Development Dependencies

Create `requirements_dev.txt` for dev-only tools like `pytest`:

```text
-r requirements.txt
pytest>=x.y.z
```

Install development requirements:
```bash
(venv) $ python -m pip install -r requirements_dev.txt
```

Install production requirements only:
```bash
(venv) $ python -m pip install -r requirements.txt
```

### Freezing Requirements for Production

Release workflow:

| Step | Command | Explanation |
|---|---|---|
| 1 | `pytest` | Run tests |
| 2 | `pip install -U -r requirements.txt` | Upgrade to match constraints |
| 3 | `pytest` | Run tests again |
| 4 | `pip freeze > requirements_lock.txt` | Freeze exact versions |

The `requirements_lock.txt` file contains exact version specifiers and can replicate your environment on other machines.

## Uninstalling Packages With pip

Before uninstalling, check dependencies with `pip show`:

```bash
(venv) $ python -m pip show requests
```

Uninstall packages:
```bash
(venv) $ python -m pip uninstall certifi
(venv) $ python -m pip uninstall urllib3 -y
(venv) $ python -m pip uninstall -y charset-normalizer idna requests
(venv) $ python -m pip uninstall -r requirements.txt -y
```

The `-y` switch suppresses confirmation dialogs.

**Note:** In a virtual environment, it can be less work to delete the environment and create a new one rather than uninstalling individual packages.

## Alternatives to pip

| Tool | Description |
|---|---|
| Conda | Package, dependency, and environment manager for many languages. From Anaconda. Operates its own index. Widely used for data science. |
| Poetry | Goes beyond package management — builds distributions and deploys to PyPI. |
| Pipenv | Merges virtual environment and package management in a single tool. |
| uv | Advertised as “Cargo for Python.” Unveiled February 2024 by Astral. Aims to be a drop-in replacement for `pip`. |

## FAQ

**What does pip stand for?**
“pip installs packages.”

**What is pip used for in Python?**
Installing and managing libraries and dependencies not included in Python’s standard library.

**Does pip come with Python?**
Yes, pip has been included with Python installers since version 3.4.

**How do you check if you have pip?**
Run `where pip3` on Windows or `which pip3` on Linux and macOS.

**How do you install packages from a requirements.txt with pip?**
Use `pip install -r requirements.txt`.

## See Also

- [Python Dependency Management](/wiki/python-programming/python-dependency-management.md)
- [Python uv: All-in-One Package and Project Manager](/wiki/python-programming/python-uv.md)
- [Virtual Environment Management](/wiki/python-programming/virtual-environment-management.md)

## Status Notes

> **Status: Draft**
> This article covers pip as Python’s standard package manager, including installation, virtual environment usage, requirements files, uninstalling, and alternatives. Content is based on Real Python’s “Using Python’s pip to Manage Your Projects’ Dependencies” tutorial.