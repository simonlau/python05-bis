# Python Dependency Management

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-02
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](/Users/simonlau/code/python05-bis/raw/python-programming/2026-11-01-the-codex-python05-bis.md)
> Updated: 2026-11-02

## Overview

Dependency management is the practice of declaring, installing, and tracking external libraries (referred to as "reagents" in The Codex) that a Python project depends on. The Codex teaches both pip (with `requirements.txt`) and Poetry (with `pyproject.toml`), highlighting their different philosophies and trade-offs.

## Package Managers Compared

### pip

pip is Python's built-in package installer. It works with `requirements.txt` files and installs packages one at a time, resolving dependencies as it goes.

**Philosophy:** Simple, direct, resolves dependencies at install time

**Key Characteristics:**
- Included with Python by default
- Resolves dependencies during installation
- Installs whatever versions satisfy constraints
- Can produce different results on different machines

### Poetry

Poetry is a modern Python dependency management and packaging tool. It works with `pyproject.toml` files and uses deterministic dependency resolution.

**Philosophy:** Deterministic, reproducible, locks dependency versions

**Key Characteristics:**
- Must be installed separately
- Resolves dependencies before installation
- Generates `poetry.lock` file with exact resolved versions
- Produces identical results on every install

## Comparison Table

| Aspect | pip (requirements.txt) | Poetry (pyproject.toml + poetry.lock) |
|--------|------------------------|--------------------------------------|
| Configuration File | `requirements.txt` | `pyproject.toml` |
| Lock File | None (optional `pip freeze`) | `poetry.lock` (always created) |
| Dependency Resolution | At install time | Before install |
| Version Pinning | Manual | Automatic via lock file |
| Reproducibility | Not guaranteed | Guaranteed with lock file |
| Virtual Environments | Manual creation | Automatic management |
| Included with Python | Yes | No, separate install |
| Project Declarations | Separate dependencies | Unified `pyproject.toml` |
| Publishing | Separate tools | Built-in |
| Resolves Conflicts | At install time | Before installation |

## How pip Works

**Installation process:**
```bash
# Install packages from requirements.txt
pip install -r ex0/requirements.txt

# Install a single package
pip install pandas==2.1.0

# List installed packages
pip freeze

# Capture current state
pip freeze > requirements.txt
```

**requirements.txt format:**
```text
pandas==2.1.0
numpy==1.25.0
requests>=2.28.0
flask==2.3.0
```

**Limitations:**
- Dependencies resolved at install time
- No lock file → different machines may get different versions
- Transitive dependencies can conflict
- `pip freeze` captures all packages, not just direct dependencies

## How Poetry Works

**Installation process:**
```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -

# Initialize a new project
poetry init

# Add dependencies
poetry add pandas numpy

# Install dependencies
poetry install

# Run commands in virtual environment
poetry run python ex0/loading.py

# Lock dependencies
poetry lock

# Update dependencies
poetry update
```

**pyproject.toml format:**
```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""

[tool.poetry.dependencies]
python = "^3.10"
pandas = "^2.1.0"
numpy = "^1.25.0"

[tool.poetry.dev-dependencies]
pytest = "^7.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**poetry.lock file:**
Contains exact resolved versions of all dependencies, including transitive dependencies. Ensures every installation produces identical results.

**Advantages:**
- Deterministic resolution before installation
- Automatic virtual environment management
- Lock file guarantees reproducibility
- Built-in project publishing
- Clear separation of dev dependencies

## The Codex Exercise 0: Part 2 - Stocking the Reagents

**Objective:** Create a program (`ex0/loading.py`) that:

1. Declares external reagents (libraries such as pandas and numpy) in both:
   - `ex0/requirements.txt` (for pip)
   - `ex0/pyproject.toml` (for Poetry)
2. Imports each declared reagent and reports its installed version
3. Shows, in its output, the difference between pip and Poetry dependency management

**Authorized Imports:** `os`, `sys`, `site`, `importlib`, `pandas`, `numpy`

**Required Behavior:**
- Must detect which reagents are available
- If one is missing, print a helpful message with install commands for both pip and Poetry
- Must not crash

**Expected Output (reagents installed):**
```
REAGENT STATUS: Loading
Checking dependencies:

[OK] pandas (2.1.0) - Data manipulation ready
[OK] numpy (1.25.0) - Numerical computation ready
All reagents present and accounted for.
```

**pip vs Poetry output comparison:**
```
pip vs numpy requirements.txt pyproject.toml versions Poetry: declares declares what the so resolve at install time; pip pins the resolved versions to same every install
```

**Testing without reagents installed:**
```bash
$> python3 ex0/loading.py
# Should show missing and installation instructions for pip and Poetry
```

**Installing with pip:**
```bash
$> pip install -r ex0/requirements.txt
$> python3 ex0/loading.py
# Should list the installed reagent versions
```

**Installing with Poetry:**
```bash
$> poetry install
$> poetry run python ex0/loading.py
# Should list the same versions as Poetry inside environment
```

## Choosing Between pip and Poetry

### Choose pip when:
- Working on simple scripts or small projects
- You need minimal tooling overhead
- You're already familiar with pip workflows
- Project doesn't require strict reproducibility

### Choose Poetry when:
- Working on larger projects or teams
- Reproducibility is critical
- You want automatic virtual environment management
- You need built-in project publishing
- You want deterministic dependency resolution

## Best Practices

### 1. Always Use Virtual Environments

Whether using pip or Poetry, always create a virtual environment:

```bash
# With pip
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# With Poetry
poetry install
poetry run python script.py
```

### 2. Pin Direct Dependencies

```text
# requirements.txt - pin exact versions
pandas==2.1.0
numpy==1.25.0
```

```toml
# pyproject.toml - use caret ranges, Poetry locks exact versions
pandas = "^2.1.0"
numpy = "^1.25.0"
```

### 3. Commit Lock Files

With Poetry, commit `poetry.lock` to version control:

```bash
# .gitignore - do NOT ignore poetry.lock
# .gitignore - DO ignore virtual environments
.venv/
venv/
```

### 4. Separate Dev Dependencies

```toml
# pyproject.toml
[tool.poetry.dev-dependencies]
pytest = "^7.0.0"
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.0.0"
```

### 5. Document Install Instructions

**pip:**
```bash
pip install -r requirements.txt
```

**Poetry:**
```bash
poetry install
poetry run python script.py
```

## Common Issues

### 1. Dependency Conflicts

**Problem:** Two packages require different versions of the same dependency
**pip solution:** May install incompatible versions or fail at install time
**Poetry solution:** Detects conflict during resolution, before installation

### 2. Transitive Dependency Hell

**Problem:** Package A requires Package B v1.0, Package C requires Package B v2.0
**Solution:** Use Poetry's deterministic resolution or carefully manage pip constraints

### 3. Missing Lock File

**Problem:** `requirements.txt` without lock file leads to non-reproducible builds
**Solution:** Use `pip freeze > requirements.txt` for snapshots, or switch to Poetry

## See Also

- [Virtual Environment Management](/wiki/python-programming/virtual-environment-management)
- [Python Package Structure Basics](/wiki/python-programming/python-package-basics)
- [Python Imports Guide](/wiki/python-programming/python-imports-guide)

## Status Notes

> **Status: Draft**
> This article covers dependency management concepts as taught in Exercise 0 of The Codex. Content may be refined based on specific exercise requirements.