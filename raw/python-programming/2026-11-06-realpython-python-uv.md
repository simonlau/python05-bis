# Managing Python Projects With uv: An All-in-One Solution

> Source: https://realpython.com/python-uv/
> Collected: 2026-11-06
> Published: 2026-10-26

# Managing Python Projects With uv: An All-in-One Solution

by Leodanis Pozo Ramos Updated Oct 26, 2026 Reading time estimate 29m

## Table of Contents

- Getting to Know uv for Python
- Installing uv to Manage Python Projects
  - Using the Standalone Installer
  - Installing From PyPI
  - Upgrading to the Latest uv Version
- Handling Python Projects With uv
  - Creating a Python Project
  - Running the Project’s Entry-Point Script
- Using uv for Dependency Management
  - Adding and Installing Dependencies
  - Upgrading and Removing Dependencies
  - Managing Development Dependencies
  - Locking and Syncing the Environment
- Building and Publishing Packages
  - Configuring the Project
  - Building a Distribution
  - Publishing a Distribution
- Conclusion
- Frequently Asked Questions

## Introduction

The uv tool is a high-speed package and project manager for Python. It’s written in Rust and designed to streamline your workflow. It offers fast dependency installation and integrates various functionalities into a single tool.

With uv, you can install and manage multiple Python versions, create virtual environments, efficiently handle project dependencies, reproduce working environments, and even build and publish a project. These capabilities make uv an all-in-one tool for Python project management.

**By the end of this tutorial, you’ll understand that:**

- **uv is a Python package and project manager** that integrates multiple functionalities into one tool, offering a comprehensive solution for managing Python projects.

- **uv is used for fast dependency installation**, virtual environment management, Python version management, and project initialization, enhancing productivity and efficiency.

- **uv can build and publish Python packages** to package repositories like PyPI, supporting a streamlined process from development to distribution.

- **uv automatically handles virtual environments**, creating and managing them as needed to ensure clean and isolated project dependencies.

## Getting to Know uv for Python

Recently, a few exciting tools built with the Rust programming language have appeared in the Python tooling ecosystem. Ruff—a linter and code formatter for Python—is a well-known and popular example of one of these tools.

In this tutorial, you’ll explore another cool tool made with Rust for Python. You’ll get to know uv, an extremely fast Python package and project manager.

The main idea behind these tools is to accelerate your Python workflow by speeding up your project management actions. For example, Ruff is 10 to 100 times faster than linters like Flake8 and code formatters like Black. Similarly, for package installation, uv is 10 to 100 times faster than pip.

Additionally, uv integrates into one tool most of the functionality provided by tools like pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more. Therefore, uv is an all-in-one solution.

### Key uv Features

- **Fast dependency installation**: Installs dependencies really fast, which is especially useful for large dependency trees.
- **Virtual environment management**: Automatically creates and manages virtual environments.
- **Python version management**: Allows the installation and management of multiple Python versions.
- **Project initialization**: Scaffolds a full Python project, including the root directory, Git repository, virtual environment, pyproject.toml, README, and more.
- **Dependency management**: Installs, updates, removes, and locks direct and transitive dependencies, which allows for environment reproducibility.
- **Package builds and publication management**: Allows you to build and publish packages to package repositories like the Python Package Index (PyPI).
- **Developer tooling support**: Installs and lets you run development tools, such as pytest, Black, and Ruff.

uv is a standalone binary that allows for a smooth installation and quick upgrades. You don’t need to have Python installed on your system to install uv.

## Installing uv to Manage Python Projects

### Using the Standalone Installer

Windows (PowerShell):
```
PS> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Linux + macOS:
```
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or with wget:
```
$ wget -qO- https://astral.sh/uv/install.sh | sh
```

To install a specific version:
```
https://astral.sh/uv/0.6.12/install.sh
```

Verify installation:
```
$ uv --version
uv 0.6.12 (e4e03833f 2025-04-02)
```

### Installing From PyPI

```
$ pipx install uv
```

### Upgrading to the Latest uv Version

If installed via standalone installer:
```
$ uv self update
```

If installed via pipx:
```
$ pipx upgrade uv
```

## Handling Python Projects With uv

### Creating a Python Project

```
$ uv init --no-package rpcats
```

This creates:
```
rpcats/
│
├── .git/
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

Initial `pyproject.toml`:
```toml
[project]
name = "rpcats"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []
```

The `.python-version` file contains the default Python version for the project. This tells uv which Python version to use when creating a dedicated virtual environment.

To manage an existing project with uv:
```
$ uv init --no-package
```

### Running the Project’s Entry-Point Script

```
$ uv run main.py
Using CPython 3.13.2
Creating virtual environment at: .venv
Hello from rpcats!
```

uv automatically creates a dedicated virtual environment and a `uv.lock` cross-platform lockfile. The `uv.lock` file uses TOML format and contains exact versions of dependencies. It should be added to version control but not edited manually.

## Using uv for Dependency Management

### Adding and Installing Dependencies

```
$ uv add requests
```

This adds `requests` to `pyproject.toml`:
```toml
[project]
name = "rpcats"
version = "0.1.0"
description = "Display cat information for the specified breed."
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "requests>=2.32.3",
]
```

`uv add` installs dependencies, edits `pyproject.toml`, and keeps `uv.lock` up-to-date. It tracks:
- **Direct dependencies**: Packages your project depends on directly
- **Transitive dependencies**: Packages that support your direct dependencies

To migrate from requirements.txt:
```
$ uv add -r requirements.txt
```

### Upgrading and Removing Dependencies

```
$ uv lock --upgrade-package requests
$ uv remove <package_name>
```

`uv remove` also removes transitive dependencies and updates `pyproject.toml` and `uv.lock`.

### Managing Development Dependencies

```
$ uv add --dev pytest
```

This adds `pytest` under `[dependency-groups]`:
```toml
[dependency-groups]
dev = [
    "pytest>=8.3.5",
]
```

### Locking and Syncing the Environment

- **Locking**: Captures specific dependencies in the lockfile for reproducibility
- **Syncing**: Installs packages from the lockfile into the project’s environment

```
$ uv lock
$ uv sync
```

`uv run` automatically locks and syncs before executing.

## Building and Publishing Packages

### Configuring the Project

Add entry-point script:
```toml
[project.scripts]
rpcats = "main:main"
```

Add build system:
```toml
[build-system]
requires = ["setuptools>=78.1.0", "wheel>=0.45.1"]
build-backend = "setuptools.build_meta"
```

### Building a Distribution

```
$ uv build
```

Builds source and binary distributions in `dist/`:
- `uv build --sdist` - source distribution only
- `uv build --wheel` - binary distribution only

### Publishing a Distribution

```
$ uv publish --index testpypi --token your_token_here
$ uv publish --token your_token_here
```

## Conclusion

**Key learnings:**

- Install uv on your operating system
- Create and manage Python projects with uv
- Handle dependencies efficiently with uv commands
- Build and publish Python packages to PyPI or private indexes
- Set up developer tools within uv for a streamlined workflow

uv is an all-in-one solution that speeds up your workflow and simplifies project management.

## Frequently Asked Questions

**How do I install uv for managing Python projects?**
You can install uv using a standalone installer or from PyPI using tools like pipx or pip. Depending on your operating system, you can also use tools like Homebrew and Cargo.

**Can uv manage virtual environments automatically?**
Yes, uv automatically creates and manages virtual environments for your projects.

**How can I build and publish a Python package using uv?**
You can build a package using the `uv build` command, and publish it to a package repository like PyPI or a private index with the `uv publish` command.

**Does uv support Python version management?**
Yes, uv allows you to install and manage multiple Python versions within your projects using the `uv python install` command.