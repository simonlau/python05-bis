# Virtual Environment Management

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-01; Real Python (Martin Breuss); 2024-11-30
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](../../raw/python-programming/2026-11-01-the-codex-python05-bis.md); [Python Virtual Environments: A Primer](../../raw/python-programming/2026-11-06-python-virtual-environments-primer.md)
> Updated: 2026-11-06

## Overview

Virtual environment management is the foundation of isolated Python development. A virtual environment creates a self-contained directory structure that isolates Python packages, dependencies, and the Python interpreter itself from the system-wide Python installation. This prevents dependency conflicts and ensures reproducible environments across different projects and machines.

The Codex refers to this concept as "The Sealed Laboratory" — a workspace sealed off from the outside world, so that a failed experiment never contaminates anything beyond its own walls. Real Python describes virtual environments as providing lightweight and isolated development environments that let you manage dependencies separately for different projects, preventing conflicts and maintaining cleaner setups.

## What Is a Virtual Environment?

### Core Definition

A Python virtual environment is a folder structure that provides everything needed to run a lightweight yet isolated Python environment. According to PEP 405, a virtual environment in its simplest form consists of:

1. A copy or symlink of the **Python binary**
2. A **`pyvenv.cfg`** configuration file
3. A **site-packages directory**

The `venv` module has been Python's officially recommended way to create virtual environments since **Python 3.5**.

### `pyvenv.cfg` Configuration

The `pyvenv.cfg` file contains key-value pairs that Python uses to set variables in the `sys` module:

```
home = /usr/local/bin
include-system-site-packages = false
version = 3.12.5
executable = /usr/local/bin/python3.12
command = /usr/local/bin/python3.12 -m venv /path/to/project/venv
```

| Setting | Purpose |
|---------|---------|
| `home` | Path to the base Python executable used to create the environment |
| `include-system-site-packages` | Whether to include base site-packages (default: `false`) |
| `version` | Python version used to create the environment |
| `executable` | Path to the Python executable |
| `command` | The venv command used to create the environment |

### Folder Structure

A virtual environment folder structure (Linux/macOS):

```
venv/
├── bin/
│   ├── activate
│   ├── activate.csh
│   ├── activate.fish
│   ├── pip
│   ├── pip3
│   ├── pip3.12
│   ├── python
│   ├── python3
│   └── python3.12
├── include/
├── lib/
│   └── python3.12/
│       └── site-packages/
├── lib64/  (symlink to lib/ on some Linux systems)
└── pyvenv.cfg
```

**Windows structure** uses `Scripts\` instead of `bin/` and `Lib\` instead of `lib/`.

### Preinstalled Packages

- **Python 3.12+**: Only `pip` is preinstalled in `site-packages/`
- **Python < 3.12**: Also included `setuptools`, `pkg_resources`, and `_distutils_hack`

## Why Use Virtual Environments?

### Avoid System Pollution

Linux and macOS come preinstalled with a version of Python that the operating system uses for internal tasks. Installing packages to your operating system's global Python mixes them with system-relevant packages, which could have unexpected side effects on tasks crucial to your operating system's normal behavior. Additionally, if you update your operating system, installed packages might get overwritten and lost.

### Sidestep Dependency Conflicts

One project might require a different version of an external library compared to another project. If you only have one place to install packages, you cannot work with two different versions of the same library.

**Example from Real Python:** One client needs Django 2.2.26 (refuses to update), another client needs Django 5.1 (for async functionality). Installing Django globally means the second installation overwrites the first. Per-project virtual environments solve this — each environment holds its own specific version of Django.

### Minimize Reproducibility Issues

If all packages live in one location, it's difficult to pin dependencies relevant for a single project. `pip freeze` outputs all installed packages, making it hard to tell which are needed for which project. Separate virtual environments make dependency pinning straightforward.

### Dodge Installation Privilege Lockouts

You may need administrator privileges to install packages into the host Python's site-packages directory. Virtual environments create a new installation location within your user privileges, allowing you to install and work with external packages without admin access.

## Creating Virtual Environments

### Basic Creation

```bash
# Create a virtual environment named "venv"
python3 -m venv venv/

# Create with a custom name
python3 -m venv lab_env/
python3 -m venv .venv/
```

### Platform-Specific Commands

**Windows:**
```powershell
py -m venv venv\
# Or with full Python path
C:\Users\Name\AppData\Local\Programs\Python\Python312\python -m venv venv\
```

**Linux/macOS:**
```bash
python3 -m venv venv/
# If python3 doesn't work, try the specific version
python3.12 -m venv venv/
```

### Customization Options

| Option | Purpose |
|--------|---------|
| `--prompt NAME` | Sets a custom command prompt name without changing folder name |
| `--clear` | Deletes contents of existing environment before recreating |
| `--upgrade-deps` | Automatically updates pip from PyPI after creation |
| `--without-pip` | Creates environment without pip (smaller, ~56K vs several MB) |
| `--system-site-packages` | Gives read access to base site-packages |
| `--symlinks` | Creates symlinks instead of copies for Python binaries |
| `--copies` | Creates copies instead of symlinks |
| `--upgrade` | Updates executables while keeping site-packages intact |

### Platform-Specific Binary Handling

- **Windows**: May create symlink or copy (symlinks may require admin privileges)
- **Linux**: Often opts for symlinks over copies
- **macOS**: Always creates copies

Symlinking is preferable where possible (per PEP 405) because base Python upgrades keep executables in sync, but symlinks can be flimsy on some systems.

## Activating Virtual Environments

### Activation Commands

**Windows (PowerShell):**
```powershell
venv\Scripts\activate
(venv) PS>
```

**Linux/macOS (Bash/Zsh):**
```bash
source venv/bin/activate
(venv) $
```

### What Activation Does

Two critical actions happen in the activation script:

1. **PATH**: Sets `VIRTUAL_ENV` to the root folder path and prepends the virtual environment's executable path to your shell `PATH`
2. **Prompt**: Changes the command prompt to show the environment name in parentheses (e.g., `(venv)`)

These changes are for convenience — you can use a virtual environment without activating it by providing the absolute path to its Python executable:

```bash
$ /home/name/path/to/venv/bin/python
```

### Running From Anywhere

Without activation, use absolute paths:
- Windows: `C:\Users\Name\path\to\venv\Scripts\python.exe`
- Linux/macOS: `/home/name/path/to/venv/bin/python`

This is useful for cron jobs, Docker containers, and scheduled scripts.

## How Virtual Environments Work Internally

### Prefix-Finding Process

Instead of looking for the `os` module to determine standard library location, the Python interpreter first looks for a `pyvenv.cfg` file. If found with a `home` key:

- `sys.base_prefix` = path to base Python executable
- `sys.prefix` = path to virtual environment directory

Without `pyvenv.cfg`, both `sys.base_prefix` and `sys.prefix` point to the same path (not a virtual environment).

When these variables differ, Python adapts module resolution:
- Standard library and header files found relative to `sys.base_prefix`
- Site-package directories found relative to `sys.prefix`

### Standard Library Linkage

Virtual environments reuse Python's built-ins and standard-library modules from the base Python installation, avoiding the overhead of copying them. This speeds up creation and makes environments more lightweight (per PEP 405 motivation).

You can optionally give access to base site-packages with `--system-site-packages`. This connection works in one direction only — new packages installed in the virtual environment won't mingle with base packages.

### site-packages Isolation

Activation replaces the default site-packages directory path in `sys.path` with the one inside your virtual environment. Python loads external packages from your virtual environment instead of the base installation. Conversely, the path to your base Python's site-packages directory is no longer in `sys.path`, so Python won't load modules from there.

## Working With Virtual Environments

### Installing Packages

After activation, install packages with pip:

```bash
(venv) $ python -m pip install <package-name>
```

Packages install into the virtual environment's isolated `site-packages/` directory, not the global location.

### Deactivating

```bash
(venv) $ deactivate
$
```

Deactivation reverses PATH and prompt changes, returning to the global Python environment.

### Treating Environments as Disposable

Virtual environments are disposable folder structures you can safely delete and recreate. Do not:

- Commit virtual environments to version control
- Ship virtual environments with your project
- Manually add code or information into a virtual environment

Anything in a virtual environment should be handled by your package manager (`pip` or `conda`).

## Managing Virtual Environments

### Where to Create Environment Folders

Two widely-held approaches:

**1. Inside each project folder:**
```
project_name/
├── venv/
└── src/
```
Advantage: Know which environment belongs to which project; activate with short relative path.

**2. In a single location:**
```
name/
├── venvs/
│   ├── django-venv/
│   ├── flask-venv/
│   └── pandas-venv/
├── projects/
│   ├── django-project/
│   └── flask-project/
```
Advantage: Single location to inspect and manage all environments.

### Pinning Dependencies

To make a virtual environment reproducible, create a `requirements.txt`:

```bash
(venv) $ python -m pip freeze > requirements.txt
```

Recreate elsewhere:
```bash
(venv) $ python -m pip install -r requirements.txt
```

**Limitations of `requirements.txt`:**
1. Doesn't include Python version information
2. May not include version information about sub-dependencies

Third-party tools address these limitations: pip-tools, Pipenv, Poetry.

### Avoid Virtual Environments in Production

Don't push `venv/` to GitHub, don't include in CI/CD pipelines, don't set up on deployment servers unless managing multiple projects yourself. Most hosting providers create isolation automatically. Use pinned dependencies (`requirements.txt`) instead of including the virtual environment folder.

## Alternatives to venv

### Virtualenv

Virtualenv is a superset of `venv` and provides the basis for its implementation. Advantages:

- Creates environments more quickly (caches platform-specific data)
- Up-to-date pip and setuptools without internet connection
- Supports Python 2.x legacy versions
- Rich programmatic API

```bash
$ virtualenv venv/
created virtual environment CPython3.12.5.final.0-64 in 214ms
```

### Conda

Conda installs any package within conda environments, not just Python packages. Packages come from repo.anaconda.com instead of PyPI. Excellent for data science projects working with Python alongside other languages.

```bash
$ conda create -n <env-name>
$ conda activate <env-name>
$ conda install numpy
$ conda deactivate
```

### Third-Party Management Tools

| Tool | Description |
|------|-------------|
| virtualenvwrapper | Extension to virtualenv for easier CLI management |
| Poetry | Deterministic dependency management with auto-generated virtual environments |
| uv | Unified Python package/dependency/virtual environment management |
| Hatch | Modern Python project manager |
| Pipenv | Creates and manages virtual environments using virtualenv |
| pipx | Install Python applications in isolated environments |
| pyenv | Manage multiple Python versions |
| pyenv-virtualenv | Combines pyenv with virtualenv |

## IDE Integration

### VS Code

1. Open your project folder
2. Open the integrated terminal (View → Terminal)
3. Create and activate a virtual environment
4. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
5. Choose *Python: Select Interpreter*
6. Select the virtual environment interpreter (`./venv/bin/python` on macOS/Linux, `.\venv\Scripts\python` on Windows)

### PyCharm

- Opening existing project with venv: PyCharm automatically recognizes and activates it
- Creating new project: PyCharm prompts to create a virtual environment (default name `.venv`)
- Adding interpreter: File → Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter

## Exercise 0 Application: The Sealed Laboratory

**Objective:** Create a program (`ex0/construct.py`) that:

1. Detects whether it's running inside a virtual environment
2. Displays information about the current Python environment
3. Provides instructions for creating and activating a virtual environment if none is detected
4. Shows the difference between global and virtual environment package locations

**Authorized Imports:** `os`, `sys`, `site`, `importlib`, `pandas`, `numpy`

**Detection Method:**
```python
import sys
import os

def is_in_virtualenv():
    return (
        hasattr(sys, 'real_prefix') or  # virtualenv
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)  # venv
    )
```

**Deliverables:** `construct.py`, `loading.py`, `requirements.txt`, `pyproject.toml`

## See Also

- [Python Package Structure Basics](/wiki/python-programming/python-package-basics.md)
- [Python Imports Guide](/wiki/python-programming/python-imports-guide.md)
- [Python Dependency Management](/wiki/python-programming/python-dependency-management.md)
- [Python Dotenv Usage](/wiki/python-programming/python-dotenv-usage.md)
- [The Codex: Packages, Environments and the Alchemist's Toolchain](/wiki/python-programming/the-codex-packages-environments-and-alchemy-toolchain.md)

## Status Notes

> **Status: Draft**
> This article consolidates virtual environment concepts from The Codex (Exercise 0) and Real Python's primer. It covers creation, activation, internal mechanics, customization, alternatives, and management best practices.