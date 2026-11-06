# Using Python's pip to Manage Your Projects' Dependencies

> Source: https://realpython.com/what-is-pip/
> Collected: 2026-11-06
> Published: 2024-12-22

# Using Python's pip to Manage Your Projects' Dependencies

by Philipp Acsany Updated Dec 22, 2024 Reading time estimate 37m

## Table of Contents

- Getting Started With pip
  - Finding pip on Your System
  - Running pip as a Module
  - Using pip in a Python Virtual Environment
  - Reinstalling pip When Errors Occur
- Installing Packages With pip
  - Using the Python Package Index (PyPI)
  - Using a Custom Package Index
  - Installing Packages From Your Git Repositories
  - Installing Packages in Editable Mode to Ease Development
- Using Requirements Files
  - Pinning Requirements
  - Fine-Tuning Requirements
  - Separating Production and Development Dependencies
  - Freezing Requirements for Production
- Uninstalling Packages With pip
- Exploring Alternatives to pip
- Conclusion
- Frequently Asked Questions

## Introduction

`pip` is the standard package manager for Python, used to install and manage libraries that aren’t part of the Python standard library. You use `pip` to manage dependencies and install packages from the Python Package Index (PyPI).

You can verify if you have `pip` by using commands like `where pip3` on Windows or `which pip3` on Linux and macOS. To install packages listed in a `requirements.txt` file, use the command `pip install -r requirements.txt`. This ensures your environment replicates the specified dependencies, maintaining consistency across different setups.

**By the end of this tutorial, you’ll understand that:**

- `pip` stands for **“pip installs packages”**, indicating its primary function.

- `pip` **manages Python packages** that aren’t part of the standard library.

- You should use `pip` whenever you need **external Python packages** for your projects.

- You can **install and uninstall packages** with `pip`.

- You use **requirements files** to manage projects’ dependencies.

You can do a lot with `pip`, but the Python community is very active and has created some neat alternatives to `pip`. You’ll learn about those later in this tutorial.

## Getting Started With pip

`pip` is a **package manager** for Python. That means it’s a tool that allows you to install and manage libraries and dependencies that aren’t distributed as part of the standard library. The name **pip** was introduced by Ian Bicking in 2008:

> I’ve finished renaming pyinstall to its new name: pip. The name pip is [an] acronym and declaration: pip installs packages.

Package management is so important that Python’s installers have included `pip` since versions 3.4 and 2.7.9, for Python 3 and Python 2, respectively. Many Python projects use `pip`, which makes it an essential tool for every Pythonista.

The concept of a package manager might be familiar to you if you’re coming from another programming language. JavaScript uses npm for package management, Ruby uses gem, and the .NET platform uses NuGet. In Python, `pip` has become the standard package manager.

### Finding pip on Your System

The Python installer gives you the option to install `pip` when installing Python on your system. In fact, the option to install `pip` with Python is checked by default, so `pip` should be ready for you to use after installing Python.

**Note:** On some Linux (Unix) systems like Ubuntu, `pip` comes in a separate package called `python3-pip`, which you need to install with `sudo apt install python3-pip`. It’s not installed by default with the interpreter.

You can verify that `pip` is available by looking for the `pip3` executable on your system:

**Windows:**
```
PS> where pip3
```

**Linux + macOS:**
```
$ which pip3
```

On Windows and Unix systems, `pip3` may be found in more than one location. This can happen when you have multiple Python versions installed.

Instead of running your system `pip` directly, you can also run it as a Python module:

```
$ python -m pip
```

The `-m` switch tells Python to run a module as an executable of the `python` interpreter. This way, you can ensure that your system default Python version runs the `pip` command.

### Running pip in a Python Virtual Environment

To avoid installing packages directly into your system Python installation, you can use a virtual environment. A virtual environment provides an isolated Python interpreter for your project. Any packages that you use inside this environment will be independent of your system interpreter. This means that you can keep your project’s dependencies separate from other projects and the system at large.

Using `pip` inside a virtual environment has three main advantages. You can:

1. Be sure that you’re using the **right Python version** for the project at hand
2. Be confident that you’re referring to the **correct `pip` instance** when running `pip` or `pip3`
3. Use a **specific package version** for your project without affecting other projects

Python has the built-in `venv` module for creating virtual environments.

**Steps to create a virtual environment and verify pip:**

**Windows:**
```
PS> python -m venv venv\
PS> venv\Scripts\activate.bat

(venv) PS>  pip3 --version
pip 24.2 from ...\lib\site-packages\pip (python 3.12)

(venv) PS>  pip --version
pip 24.2 from ...\lib\site-packages\pip (python 3.12)
```

**Linux + macOS:**
```
$ python -m venv venv/
$ source venv/bin/activate

(venv) $ pip3 --version
pip 24.2 from .../python3.12/site-packages/pip (python 3.12)

(venv) $ pip --version
pip 24.2 from .../python3.12/site-packages/pip (python 3.12)
```

Once your virtual environment is activated, you can use either `pip` or `pip3`. For consistency, you can also continue to use `python -m pip` inside the virtual environment.

### Reinstalling pip When Errors Occur

When you run the `pip` command, you may get an error:

| Operating System | Error Message |
| --- | --- |
| Windows | `'pip' is not recognized as an internal or external command, operable program or batch file.` |
| Linux | `bash: pip: command not found` |
| macOS | `zsh: command not found: pip` |

These errors indicate that your system can’t find `pip` in the locations listed in your `PATH` variable.

**Supported methods to reinstall pip:**

1. The `ensurepip` module (part of the standard library since Python 3.4)
2. The `get-pip.py` script

**Using ensurepip:**
```bash
$ python -m ensurepip --upgrade
```

The `ensurepip` module doesn’t access the Internet. The latest version of `pip` that `ensurepip` can install is the version that’s bundled in your environment’s Python installation. For example, running `ensurepip` with Python 3.12 installs `pip` 24.2. If you want a newer `pip` version, then you’d need to first run `ensurepip`. Afterward, you can update `pip` manually to its latest version.

**Using get-pip.py:**
```bash
$ python get-pip.py
```

This script installs the latest version of `pip`, `setuptools`, and `wheel` in your current Python environment. If you only want to install `pip`, then you can add the `--no-setuptools` and `--no-wheel` options.

## Installing Packages With pip

Python is considered a **batteries included** language. This means that the Python standard library contains an extensive set of packages and modules. At the same time, Python has an active community that contributes an even more extensive set of packages published to the Python Package Index (**PyPI**).

### Using the Python Package Index (PyPI)

PyPI hosts an extensive collection of packages, including development frameworks, tools, and libraries. One example is the `requests` library.

To install packages, `pip` provides an `install` command:

```bash
(venv) $ python -m pip install requests
```

The `pip install <package>` command always looks for the latest version of the package and installs it. It also searches for dependencies listed in the package metadata and installs them to ensure that the package has all the requirements it needs.

You can install multiple packages in a single command:
```bash
(venv) $ python -m pip install rptree codetiming
```

To display installed packages:
```bash
(venv) $ python -m pip list
```

To get more information about a specific package:
```bash
(venv) $ python -m pip show requests
```

The output lists the package’s metadata, including the `Requires` line which lists packages the package depends on.

### Using a Custom Package Index

By default, `pip` uses PyPI to look for packages. But `pip` also gives you the option to define a custom package index.

A custom package index must comply with PEP 503 – Simple Repository API to work with `pip`. You can target a custom index with the `--index-url` option (or `-i` shorthand):

```bash
(venv) $ python -m pip install -i https://test.pypi.org/simple/ rptree
```

If you need to use an alternative index permanently, you can set the `index-url` option in the `pip` configuration file (`pip.conf`):

```ini
[global]
index-url = https://test.pypi.org/simple/
```

### Installing Packages From Git Repositories

`pip` also provides the option to install packages from a Git repository:

```bash
(venv) $ python -m pip install git+https://github.com/realpython/rptree
```

With the `git+https` scheme, you can point to a Git repository that contains an installable package. `pip` also supports Mercurial, Subversion, and Bazaar.

### Installing Packages in Editable Mode

When working on your own package, installing it in editable mode makes sense:

```bash
$ git clone https://github.com/realpython/rptree
$ cd rptree
$ python -m venv venv/
$ source venv/bin/activate
(venv) $ python -m pip install -e .
```

The `-e` option is shorthand for `--editable`. When you use the `-e` option with `pip install`, you tell `pip` that you want to install the package in editable mode. Instead of using a package name, you use a dot (`.`) to point `pip` to the current directory.

When you install a package in editable mode, you’re creating a link in the site-packages to the local project path:
```
 ~/rptree/venv/lib/python3.12/site-packages/rptree.egg-link
```

## Using Requirements Files

The `pip install` command by default installs the latest published version of a package, but sometimes your code requires a specific package version to work correctly.

### Pinning Requirements

You’ll often find Python projects that pin their requirements in a file called `requirements.txt`. The requirements file format allows you to specify precisely which packages and versions should be installed.

You can generate a requirements file using `pip freeze`:

```bash
(venv) $ python -m pip freeze > requirements.txt
```

Example `requirements.txt`:
```
certifi==x.y.z
charset-normalizer==x.y.z
idna==x.y.z
requests==x.y.z
urllib3==x.y.z
```

To replicate the environment in another system:
```bash
(venv) $ python -m pip install -r requirements.txt
```

### Fine-Tuning Requirements

You can specify dependency versions using comparison operators:

```text
certifi>=x.y.z
charset-normalizer>=x.y.z
idna>=x.y.z
requests>=x.y.z
urllib3>=x.y.z
```

Using `>=` tells `pip` to install an exact or greater version. To upgrade packages:
```bash
(venv) $ python -m pip install -U -r requirements.txt
```

To fine-tune and prevent incompatible versions:
```text
requests>=x.y.z, <3.0
```

### Separating Production and Development Dependencies

Not all packages are production dependencies. For example, `pytest` is a development dependency.

Create a second requirements file, `requirements_dev.txt`:

```text
-r requirements.txt
pytest>=x.y.z
```

Install both files in development:
```bash
(venv) $ python -m pip install -r requirements_dev.txt
```

Install only production requirements:
```bash
(venv) $ python -m pip install -r requirements.txt
```

### Freezing Requirements for Production

A workflow to create a new release:

| Step | Command | Explanation |
| --- | --- | --- |
| 1 | `pytest` | Run your tests |
| 2 | `pip install -U -r requirements.txt` | Upgrade requirements to match constraints |
| 3 | `pytest` | Run tests again |
| 4 | `pip freeze > requirements_lock.txt` | Freeze dependencies for production |

Freezing your requirements ensures that your Python project works the same way for your users as it did in your environment.

## Uninstalling Packages With pip

Before you uninstall a package, run the `show` command to check its dependencies:

```bash
(venv) $ python -m pip show requests
```

Then remove packages using the `uninstall` command:

```bash
(venv) $ python -m pip uninstall certifi
(venv) $ python -m pip uninstall urllib3 -y
(venv) $ python -m pip uninstall -y charset-normalizer idna requests
(venv) $ python -m pip uninstall -r requirements.txt -y
```

**Note:** If you’re working in a virtual environment, it can be less work to just delete your virtual environment and create a new one.

## Exploring Alternatives to pip

The Python community provides excellent tools beyond `pip`:

| Tool | Description |
| --- | --- |
| Conda | Package, dependency, and environment manager for many languages. Comes from Anaconda. Operates its own index. Widely used for data science. |
| Poetry | Goes beyond package management, helping you build distributions and deploy to PyPI. |
| Pipenv | Merges virtual environment and package management in a single tool. |
| uv | Advertised as a Cargo for Python. Unveiled in February 2024 by Astral. Aims to become a drop-in replacement for pip. |

Only `pip` comes bundled in the standard Python installation.

## Conclusion

**Key learnings:**

- Set up and run `pip` in your working environment
- Fix common errors related to working with `pip`
- Install and uninstall packages with `pip`
- Define requirements for your projects and applications
- Pin dependencies in requirements files

## Frequently Asked Questions

**What does `pip` stand for?**
`pip` stands for “pip installs packages.”

**What is `pip` used for in Python?**
You use pip to install and manage libraries and dependencies that aren’t included in Python’s standard library.

**Does `pip` come with Python?**
Yes, `pip` has been included with Python installers since version 3.4.

**How do you check if you have `pip`?**
Run `where pip3` on Windows or `which pip3` on Linux and macOS.

**How can you install packages from a `requirements.txt` with `pip`?**
Use `pip install -r requirements.txt`.