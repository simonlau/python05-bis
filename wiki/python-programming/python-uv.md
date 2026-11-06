# Python uv: All-in-One Package and Project Manager

> Sources: Real Python (Leodanis Pozo Ramos); 2026-10-26
> Raw: [Managing Python Projects With uv: An All-in-One Solution](../../raw/python-programming/2026-11-06-realpython-python-uv.md)
> Updated: 2026-11-06

## Overview

uv is a high-speed package and project manager for Python written in Rust. It integrates multiple functionalities into a single tool, offering fast dependency installation, virtual environment management, Python version management, project initialization, dependency locking, and package building and publishing.

uv replaces or integrates the functionality of tools like `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `twine`, and `virtualenv`. It is an all-in-one solution for Python project management.

## Key Features

| Feature | Description |
|---------|-------------|
| Fast dependency installation | 10–100x faster than pip for package installation |
| Virtual environment management | Automatically creates and manages virtual environments |
| Python version management | Installs and manages multiple Python versions |
| Project initialization | Scaffolds full Python project with Git, venv, pyproject.toml, README |
| Dependency management | Installs, updates, removes, and locks direct and transitive dependencies |
| Package builds and publication | Builds and publishes packages to PyPI or private indexes |
| Developer tooling | Runs development tools like pytest, Black, Ruff |
| Standalone binary | No Python required to install; quick upgrades |

## Installing uv

### Standalone Installer

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux + macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or with wget:
```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

To install a specific version, add the version number to the URL:
```
https://astral.sh/uv/0.6.12/install.sh
```

Verify:
```bash
uv --version
# uv 0.6.12 (e4e03833f 2025-04-02)
```

### From PyPI

```bash
pipx install uv
```

### Upgrading

```bash
# Standalone installer
uv self update

# pipx
pipx upgrade uv
```

## Creating a Python Project

```bash
uv init --no-package rpcats
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

The `.python-version` file specifies the default Python version for the project. The initial `pyproject.toml`:

```toml
[project]
name = "rpcats"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []
```

To manage an existing project:
```bash
uv init --no-package
```

## Running Project Scripts

```bash
uv run main.py
```

uv automatically:
1. Detects or installs the Python version from `.python-version`
2. Creates a dedicated virtual environment at `.venv/`
3. Generates a `uv.lock` cross-platform lockfile
4. Installs dependencies from `uv.lock`
5. Runs the script

The `uv.lock` file should be added to version control but not edited manually.

## Dependency Management

### Adding Dependencies

```bash
uv add requests
```

This:
1. Adds `requests>=2.32.3` to `pyproject.toml` dependencies
2. Installs `requests` and its transitive dependencies
3. Updates `uv.lock` with exact versions

Migrate from `requirements.txt`:
```bash
uv add -r requirements.txt
```

### Upgrading Dependencies

```bash
uv lock --upgrade-package requests
```

### Removing Dependencies

```bash
uv remove <package_name>
```

Removes the package and its transitive dependencies, updating `pyproject.toml` and `uv.lock`.

### Development Dependencies

```bash
uv add --dev pytest
```

Adds to `[dependency-groups]` in `pyproject.toml`:
```toml
[dependency-groups]
dev = [
    "pytest>=8.3.5",
]
```

### Locking and Syncing

- **Locking**: Captures specific dependencies in `uv.lock` for reproducibility
- **Syncing**: Installs packages from `uv.lock` into the project environment

```bash
uv lock
uv sync
```

`uv run` automatically locks and syncs before executing.

## Python Version Management

uv can install and manage multiple Python versions:

```bash
uv python install
```

uv uses distributions from the Astral project (Python doesn't publish official distributable binaries).

## Building and Publishing Packages

### Configuring the Project

Add an entry-point script:
```toml
[project.scripts]
rpcats = "main:main"
```

Add a build system:
```toml
[build-system]
requires = ["setuptools>=78.1.0", "wheel>=0.45.1"]
build-backend = "setuptools.build_meta"
```

### Building Distributions

```bash
uv build
```

Builds both source and binary distributions in `dist/`:
- `uv build --sdist` — source distribution only
- `uv build --wheel` — binary distribution only

### Publishing

```bash
# Publish to TestPyPI
uv publish --index testpypi --token your_token_here

# Publish to PyPI
uv publish --token your_token_here
```

## uv vs pip: Key Differences

| Aspect | pip | uv |
|--------|-----|-----|
| Language | Python | Rust |
| Speed | Baseline | 10–100x faster |
| Lock file | None (optional `pip freeze`) | `uv.lock` (automatic) |
| Virtual environments | Manual | Automatic |
| Python version management | No | Yes |
| Package publishing | Requires twine | Built-in (`uv publish`) |
| Dev dependencies | Manual | `--dev` flag |
| pyproject.toml support | Limited | Native |

## See Also

- [Python Dependency Management](/wiki/python-programming/python-dependency-management.md)
- [Virtual Environment Management](/wiki/python-programming/virtual-environment-management.md)
- [Python Package Structure Basics](/wiki/python-programming/python-package-basics.md)

## Status Notes

> **Status: Draft**
> This article covers uv as an all-in-one Python package and project manager. It may be updated as uv evolves and as additional comparison points with other tools are added.