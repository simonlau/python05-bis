# Python Virtual Environments: A Primer

> Source: https://realpython.com/python-virtual-environments-a-primer/
> Collected: 2026-11-06
> Published: 2024-11-30

Python Virtual Environments: A Primer

by Martin Breuss Updated Nov 30, 2024 Reading time estimate 1h 37m

## Table of Contents

- How Can You Work With a Python Virtual Environment?
  - Create It
  - Activate It
  - Install Packages Into It
  - Deactivate It
- How Do You Enable a Venv in Your IDE?
  - Create and Activate a Virtual Environment in VS Code
  - Create and Activate a Virtual Environment in PyCharm
- Why Do You Need Virtual Environments?
  - Avoid System Pollution
  - Sidestep Dependency Conflicts
  - Minimize Reproducibility Issues
  - Dodge Installation Privilege Lockouts
- What Is a Python Virtual Environment?
  - A Folder Structure
  - An Isolated Python Installation
- How Does a Virtual Environment Work?
  - It Copies Structure and Files
  - It Adapts the Prefix-Finding Process
  - It Links Back to Your Standard Library
  - It Modifies Your PYTHONPATH
  - It Changes Your Shell PATH Variable on Activation
  - It Runs From Anywhere With Absolute Paths
- How Can You Customize a Virtual Environment?
  - Change the Command Prompt
  - Overwrite Existing Environments
  - Create Multiple Virtual Environments at Once
  - Update the Core Dependencies
  - Avoid Installing pip
  - Include the System Site-Packages
  - Copy or Link Your Executables
  - Upgrade Your Python to Match the System Python
- What Other Popular Options Exist, Aside From venv?
  - The Virtualenv Project
  - The Conda Package and Environment Manager
- How Can You Manage Your Virtual Environments?
  - Decide Where to Create Your Environment Folders
  - Treat Them as Disposables
  - Pin Your Dependencies
  - Avoid Virtual Environments in Production
  - Use Third-Party Tools
- Conclusion
- Frequently Asked Questions

## Introduction

Creating a Python virtual environment allows you to manage dependencies separately for different projects, preventing conflicts and maintaining cleaner setups. With Python's `venv` module, you can create isolated environments that use different versions of libraries or Python itself. This tutorial guides you through creating, activating, and managing these environments efficiently.

**By the end of this tutorial, you'll understand that:**

- Python virtual environments provide **lightweight and isolated** Python development environments.
- You can use Python's **`venv` module** to manage dependencies **independently for each project**.
- You create and **set up a venv in Python** using the command `python -m venv path/to/venv/`.
- You **refer** to a virtual environment by the **folder name** that you used when creating the venv.
- You **activate a venv on Windows** with `venv\Scripts\activate`, and **on macOS and Linux** with `source venv/bin/activate`.
- You can **enable a venv in VS Code** by opening the Command Palette and choosing *Python: Select Interpreter*.

Working with virtual environments is a common and effective practice in Python development. Gaining a better understanding of how they work, why you need them, and what you can do with them will help you master your Python programming workflow.

## How Can You Work With a Python Virtual Environment?

This tutorial uses Python's `venv` module to create virtual environments. This module is part of Python's standard library, and it's been the officially recommended way to create virtual environments since Python 3.5.

**Note:** There are other great third-party tools for creating virtual environments, such as conda and virtualenv, that you'll learn more about later in this tutorial. Either of these tools can help you set up a virtual environment and also go beyond just that.

For basic usage, `venv` is an excellent choice because it already comes packaged with your Python installation.

### Create It

Any time you're working on a Python project that uses external dependencies you're installing with pip, it's best to first create a virtual environment:

Windows:
```
PS> py -m venv venv\
```

Linux/macOS:
```
$ python3 -m venv venv/
```

This command creates a new virtual environment named `venv` using Python's built-in `venv` module. The first `venv` specifies the module, and the second `venv/` sets the name for your virtual environment.

### Activate It

Great! Your project now has its own virtual environment. Generally, before you start to use it, you'll **activate** the environment by executing a script:

Windows:
```
PS> venv\Scripts\activate
(venv) PS>
```

Linux + macOS:
```
$ source venv/bin/activate
(venv) $
```

Once you can see the name of your virtual environment in your command prompt—in this case `(venv)`—then you know that your virtual environment is active.

### Install Packages Into It

After you've created and activated your virtual environment, you can install any external dependencies:

```
(venv) $ python -m pip install <package-name>
```

Because you first created and activated the virtual environment, pip will install the packages in an isolated location. Every Python package you install will end up in this isolated environment instead of your global Python site-packages.

### Deactivate It

Once you're done working with this virtual environment:

```
(venv) $ deactivate
$
```

## How Do You Enable a Venv in Your IDE?

### VS Code

1. Open Your Workspace
2. Open the Integrated Terminal
3. Create a Virtual Environment with `venv`
4. Activate the Virtual Environment
5. Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and choose *Python: Select Interpreter*
6. Select the virtual environment interpreter (path shows as `.\venv\Scripts\python` on Windows or `./venv/bin/python` on macOS and Linux)

### PyCharm

- Opening an existing project with a virtual environment: PyCharm automatically recognizes and activates it
- Creating a new project: PyCharm prompts you to create a virtual environment, default name `.venv`
- Adding an interpreter: File → Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter

## Why Do You Need Virtual Environments?

Python isn't great at dependency management. If you're not specific, pip will place all external packages in a folder called `site-packages/` in your base Python installation.

### Avoid System Pollution

Linux and macOS come preinstalled with a version of Python that the operating system uses for internal tasks. Installing packages to your operating system's global Python mixes them with system-relevant packages, which could have unexpected side effects. If you update your operating system, installed packages might get overwritten and lost.

### Sidestep Dependency Conflicts

One project might require a different version of an external library compared to another project. If you only have one place to install packages, you won't be able to work with two different versions of the same library.

Example: One client needs Django 2.2.26, another needs Django 5.1 (for async functionality). Installing Django globally means only one version can exist—the second installation overwrites the first. Per-project virtual environments solve this.

### Minimize Reproducibility Issues

If all packages live in one location, it's difficult to pin dependencies relevant for a single project. With separate virtual environments, you can more easily share your project requirements using `pip freeze`.

### Dodge Installation Privilege Lockouts

You may need administrator privileges to install packages into the host Python's site-packages directory. Virtual environments create a new installation location within your user privileges, allowing you to install and work with external packages.

## What Is a Python Virtual Environment?

A Python virtual environment is a folder structure that gives you everything you need to run a lightweight yet isolated Python environment.

### A Folder Structure

The three essential parts:
1. A copy or symlink of the **Python binary**
2. A **`pyvenv.cfg`** file
3. A **site-packages directory**

`pyvenv.cfg` example:
```
home = /usr/local/bin
include-system-site-packages = false
version = 3.12.5
executable = /usr/local/bin/python3.12
command = /usr/local/bin/python3.12 -m venv /path/to/project/venv
```

Folder structure (Linux/macOS):
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
├── lib64/ (symlink to lib/ on some Linux systems)
└── pyvenv.cfg
```

### An Isolated Python Installation

Virtual environments aim to provide a lightweight, isolated Python environment. They reproduce the folder structure of a standard Python installation.

Starting with Python 3.12, virtual environments come preinstalled with only one dependency: `pip`. Older versions also included setuptools, pkg_resources, and _distutils_hack.

## How Does a Virtual Environment Work?

### It Copies Structure and Files

`venv` re-creates the file and folder structure of a standard Python installation, copying or symlinking the Python executable into that structure.

### It Adapts the Prefix-Finding Process

Instead of looking for the `os` module to determine the location of the standard library, the Python interpreter first looks for a `pyvenv.cfg` file. If found with a `home` key:

- `sys.base_prefix` = path to base Python executable
- `sys.prefix` = path to virtual environment directory

Without `pyvenv.cfg`, both point to the same path (not a virtual environment).

### It Links Back to Your Standard Library

Virtual environments reuse Python's built-ins and standard-library modules from the base Python installation, avoiding the overhead of copying them. This speeds up creation and makes environments more lightweight (per PEP 405 motivation).

You can optionally give access to base site-packages with `--system-site-packages`.

### It Modifies Your PYTHONPATH

Activation replaces the default site-packages directory path with the one inside your virtual environment. Python loads external packages from your virtual environment instead of the base installation.

### It Changes Your Shell PATH Variable on Activation

Activation:
1. Sets `VIRTUAL_ENV` variable to root folder path
2. Prepends virtual environment executable path to `PATH`
3. Changes command prompt to show environment name in parentheses

### It Runs From Anywhere With Absolute Paths

You don't need to activate a virtual environment to use it. Pass the absolute path to the Python executable inside your virtual environment:

```
$ /home/name/path/to/venv/bin/python
```

## How Can You Customize a Virtual Environment?

### Change the Command Prompt

Common folder names: `venv`, `env`, `.venv`. Use `--prompt` to set a custom command prompt name without changing the folder name.

### Overwrite Existing Environments

Running `python -m venv venv/` on an existing environment does nothing. Use `--clear` to delete contents before recreating.

### Create Multiple Virtual Environments at Once

```
$ python3 -m venv venv/ /path/to/another-venv/
```

### Update the Core Dependencies

Use `--upgrade-deps` to have pip contact PyPI and update itself right after installation.

### Avoid Installing pip

Use `--without-pip` to create a virtual environment without pip (smaller, ~56K vs several MB).

### Include the System Site-Packages

Use `--system-site-packages` to set `include-system-site-packages = true` in pyvenv.cfg, giving read access to base site-packages.

### Copy or Link Your Executables

- Windows: may create symlink or copy
- Linux: often opts for symlinks
- macOS: always creates copies

Use `--symlinks` or `--copies` to override defaults.

### Upgrade Your Python to Match the System Python

Use `--upgrade` to update executables while keeping site-packages intact.

## What Other Popular Options Exist, Aside From venv?

### The Virtualenv Project

Virtualenv is a superset of `venv` and provides the basis for its implementation. Advantages over venv:
- Creates environments more quickly (caches platform-specific data)
- Up-to-date pip and setuptools without internet connection
- Supports Python 2.x legacy versions
- Rich programmatic API

```
$ virtualenv venv/
created virtual environment CPython3.12.5.final.0-64 in 214ms
```

### The Conda Package and Environment Manager

Conda installs any package within conda environments, not just Python packages. Packages come from repo.anaconda.com instead of PyPI. Excellent for data science projects working with Python alongside other languages.

```
$ conda create -n <venv-name>
$ conda activate <venv-name>
$ conda install numpy
$ conda deactivate
```

## How Can You Manage Your Virtual Environments?

### Decide Where to Create Your Environment Folders

Two approaches:
1. Inside each project folder (alongside code)
2. In a single location (e.g., subfolder of home directory)

### Treat Them as Disposables

Virtual environments are disposable folder structures. Don't commit to version control, don't ship with project. They rely on base Python's standard library, so they're not portable applications.

### Pin Your Dependencies

Create `requirements.txt` with `pip freeze > requirements.txt`. Recreate with `pip install -r requirements.txt`.

Note: requirements.txt isn't deterministic (no Python version info, sub-dependencies may vary). Third-party tools address this: pip-tools, Pipenv, Poetry.

### Avoid Virtual Environments in Production

Don't push venv/ to GitHub, don't include in CI/CD pipelines, don't set up on deployment servers unless managing multiple projects. Hosting providers typically create isolation automatically.

### Use Third-Party Tools

- **virtualenvwrapper**: extension to virtualenv for easier management
- **Poetry**: deterministic dependency management with auto-generated virtual environments
- **uv**: unified Python package/dependency/virtual environment management
- **Hatch**: modern Python project manager
- **Pipenv**: creates and manages virtual environments using virtualenv
- **pipx**: install Python applications in isolated environments
- **pyenv**: manage multiple Python versions
- **pyenv-virtualenv**: combines pyenv with virtualenv

## Conclusion

Key learnings: create and activate virtual environments, explain why isolation matters, visualize what Python does when creating a virtual environment, customize using optional venv arguments, deactivate and remove environments, choose additional tools for managing Python versions and virtual environments.

## Frequently Asked Questions

**How do you create a Python virtual environment?**
Use `python -m venv venv/`.

**Why should you use virtual environments in Python?**
To manage dependencies for different projects separately, preventing conflicts and keeping global Python environment clean.

**How do you activate a virtual environment on Windows?**
Run `venv\Scripts\activate`.

**Can you use different versions of Python in virtual environments?**
Yes, specify the Python interpreter path when creating.

**How do you install packages in a Python virtual environment?**
Run `python -m pip install <package-name>` after activation.