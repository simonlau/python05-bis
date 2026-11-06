# Python import: Advanced Techniques and Tips

> Source: https://realpython.com/python-import/
> Collected: 2026-11-06
> Published: 2020-07-08

# Python import: Advanced Techniques and Tips

by Geir Arne Hjelle Updated Jul 08, 2020 Reading time estimate 1h 32m

## Table of Contents

- Basic Python import
  - Modules
  - Packages
  - Absolute and Relative Imports
  - Python’s Import Path
  - Example: Structure Your Imports
  - Create and Install a Local Package
  - Namespace Packages
  - Imports Style Guide
- Resource Imports
  - Introducing importlib.resources
  - Example: Use Data Files
  - Example: Add Icons to Tkinter GUIs
- Dynamic Imports
  - Using importlib
  - Example: Factory Method With Namespace Packages
  - Example: A Package of Plugins
- The Python Import System
  - Import Internals
  - Example: Singletons as Modules
  - Reloading Modules
  - Finders and Loaders
  - Example: Automatically Install From PyPI
  - Example: Import Data Files
- Import Tips and Tricks
  - Handle Packages Across Python Versions
  - Handle Missing Packages: Use an Alternative
  - Handle Missing Packages: Use a Mock Instead
  - Import Scripts as Modules
  - Run Python Scripts From ZIP Files
  - Handle Cyclical Imports
  - Profile Imports
- Conclusion

## Introduction

In Python, you use the **`import`** keyword to make code in one **module** available in another. Imports in Python are important for **structuring your code** effectively. Using imports properly will make you more productive, allowing you to reuse code while keeping your projects maintainable.

**In this tutorial, you’ll learn how to:**

- Use **modules**, **packages**, and **namespace packages**
- Handle **resources** and **data files** inside your packages
- Import modules **dynamically** at runtime
- **Customize** Python’s import system

## Basic Python import

### Modules

The Python.org glossary defines **module** as:

> An object that serves as an organizational unit of Python code. Modules have a namespace containing arbitrary Python objects. Modules are loaded into Python by the process of importing.

In practice, a module usually corresponds to one `.py` file containing Python code.

```python
>>> import math
>>> math.pi
3.141592653589793
```

`math` is part of Python’s standard library, which means it’s always available to import. `math` also acts as a namespace that keeps all attributes together.

You can list the contents of a namespace with `dir()`:

```python
>>> import math
>>> dir(math)
['__doc__', ..., 'nan', 'pi', 'pow', ...]
```

You can import only specific parts of a module:

```python
>>> from math import pi
>>> pi
3.141592653589793
>>> math.pi
NameError: name 'math' is not defined
```

Note that this places `pi` in the global namespace and not within a `math` namespace.

You can also rename modules and attributes as they’re imported:

```python
>>> import math as m
>>> m.pi
3.141592653589793

>>> from math import pi as PI
>>> PI
3.141592653589793
```

The module namespace is implemented as a Python dictionary and is available at `.__dict__`:

```python
>>> import math
>>> math.__dict__["pi"]
3.141592653589793
```

### Packages

A package is a Python module that can contain submodules or recursively, subpackages. Technically, a package is a Python module with an `__path__` attribute.

A package typically corresponds to a directory containing Python files and other directories. To create a Python package, create a directory and a file named `__init__.py` inside it. The `__init__.py` file contains the contents of the package when treated as a module. It can be left empty.

**Note:** Directories without an `__init__.py` file are still treated as packages by Python but are called **namespace packages**.

Submodules and subpackages aren’t imported when you import a package. However, you can use `__init__.py` to include any or all submodules and subpackages.

Example package structure:

```
world/
│
├── africa/
│   ├── __init__.py
│   └── zimbabwe.py
│
├── europe/
│   ├── __init__.py
│   ├── greece.py
│   ├── norway.py
│   └── spain.py
│
└── __init__.py
```

### Absolute and Relative Imports

Relative imports use a dot (`.`):

```python
from . import africa
```

You can read this as “From the current package, import the subpackage `africa`.”

The equivalent absolute import:

```python
from world import africa
```

Relative imports must be in the form `from...import`, and the location must start with a dot.

PEP 8 recommends using absolute imports in general. Relative imports are an alternative for organizing package hierarchies.

### Python’s Import Path

Python looks for modules and packages in its **import path** — a list of locations searched for modules to import.

When you type `import something`, Python looks in:
1. A module cache to see if `something` has already been imported
2. Built-in modules
3. The import path (`sys.path`)

The import path broadly contains three kinds of locations:
1. The directory of the current script (or current directory)
2. The contents of the `PYTHONPATH` environment variable
3. Other installation-dependent directories

Python searches from the beginning of the list until the first match.

**Warning:** Don’t create modules that **shadow** other important modules (e.g., naming a local file `math.py` shadows the standard library `math` module).

### Example: Structure Your Imports

Organize imports into groups:
1. Standard library imports
2. Third-party imports
3. Local application or library imports

Example:

```python
# Standard library imports
import sys
from typing import Dict, List

# Third party imports
import feedparser
import html2text

# Reader imports
from reader import URL
```

PEP 8 recommendations for import style:
- Keep imports at the top of the file.
- Write imports on separate lines.
- Organize imports into groups.
- Order imports alphabetically within each group.
- Prefer absolute imports over relative imports.
- Avoid wildcard imports like `from module import *`.

Tools: `isort` and `reorder-python-imports`.

### Create and Install a Local Package

Create minimal `setup.cfg` and `setup.py` files:

```ini
# setup.cfg
[metadata]
name = local_structure
version = 0.1.0

[options]
packages = structure
```

```python
# setup.py
import setuptools
setuptools.setup()
```

Install locally with pip:
```bash
$ python -m pip install -e .
```

The `-e` option stands for **editable**, allowing you to change source code without reinstalling.

### Namespace Packages

Namespace packages have been available since Python 3.3. They’re less dependent on the underlying file hierarchy and can be split across multiple directories. A namespace package is created automatically if you have a directory containing a `.py` file but no `__init__.py`. See PEP 420.

### Imports Style Guide

Keep imports at top of file, write on separate lines, organize into groups (stdlib, third-party, local), order alphabetically, prefer absolute imports, avoid wildcard imports.

## Resource Imports

Sometimes code depends on data files or other resources. `importlib.resources` gives access to resources within packages. It became part of the standard library in Python 3.7.

A **resource** is any file located within an importable package. Resource files must be inside a regular package (directory with `__init__.py`). Namespace packages aren’t supported.

```python
from importlib import resources

# Open text file
with resources.open_text("books", "alice_in_wonderland.txt") as fid:
    alice = fid.readlines()

# Open binary file
with resources.open_binary("books", "alice_in_wonderland.png") as fid:
    cover = fid.read()
```

Convenient functions `read_text()` and `read_binary()` are also available.

For older Python versions, install `importlib_resources` backport:
```bash
$ python -m pip install importlib_resources
```

### Example: Use Data Files

```python
import csv
from importlib import resources

def read_population_file(year, variant="Medium"):
    population = {}
    with resources.open_text("data", "WPP2019_TotalPopulationBySex.csv") as fid:
        rows = csv.DictReader(fid)
        for row in rows:
            if row["Time"] == year and row["Variant"] == variant:
                pop = round(float(row["PopTotal"]) * 1000)
                population[row["Location"]] = pop
    return population
```

### Example: Add Icons to Tkinter GUIs

Use `resources.path()` to get a path to resource files:

```python
with resources.path("hello_gui.gui_resources", "logo.png") as path:
    self._icon = tk.PhotoImage(file=path)
self.iconphoto(True, self._icon)
```

## Dynamic Imports

### Using importlib

The `importlib` package provides programmatic access to the import machinery:

```python
import importlib
module = importlib.import_module("math")
print(module.__doc__)
```

`import_module()` returns a module object that you can bind to any variable.

### Example: Factory Method With Namespace Packages

```python
import importlib

def get_serializer(format):
    try:
        module = importlib.import_module(f"serializers.{format}")
        serializer = getattr(module, f"{format.title()}Serializer")
    except (ImportError, AttributeError):
        raise ValueError(f"Unknown format {format!r}") from None
    return serializer()
```

### Example: A Package of Plugins

Use `importlib.import_module()` to dynamically load plugins, and `importlib.resources.contents()` to list all available plugins in a package.

## The Python Import System

### Import Internals

When you import a module, three things happen:
1. **Searched for** — Python looks in the module cache, then using finders
2. **Loaded** — Python loads the module using a loader
3. **Bound to a namespace** — The module is bound to a namespace

`sys.modules` acts as a module cache — it contains references to all modules that have been imported. The first place Python looks for modules is `sys.modules`.

`sys.meta_path` controls which finders are called during the import process:
```python
>>> import sys
>>> sys.meta_path
[<class '_frozen_importlib.BuiltinImporter'>,
 <class '_frozen_importlib.FrozenImporter'>,
 <class '_frozen_importlib_external.PathFinder'>]
```

Built-in modules aren’t shadowed by local modules because the built-in finder is called before the import path finder.

### Example: Singletons as Modules

Modules can serve as singletons — instantiate a class when you load the module, and the module cache ensures it’s instantiated only once.

### Reloading Modules

Use `importlib.reload()` to reload a module without restarting the interpreter:

```python
>>> import importlib
>>> importlib.reload(number)
```

`reload()` requires a module object, not a string.

### Finders and Loaders

Extend the Python import system by implementing your own finder and loader. `sys.meta_path` controls which finders are called.

Finders implement `.find_spec()` which can:
1. Return `None` if it doesn’t know how to find the module
2. Return a module spec specifying how to load the module
3. Raise `ModuleNotFoundError`

### Example: Automatically Install From PyPI

A finder can attempt to install missing modules using pip:

```python
class PipFinder:
    @classmethod
    def find_spec(cls, name, path, target=None):
        cmd = f"{sys.executable} -m pip install {name}"
        subprocess.run(cmd.split(), check=True)
        return util.find_spec(name)
```

**Warning:** The import name doesn’t always correspond to the PyPI package name. Use only in controlled environments.

### Example: Import Data Files

Implement custom finders and loaders to import CSV files directly as modules.

## Import Tips and Tricks

### Handle Packages Across Python Versions

```python
try:
    from importlib import resources
except ModuleNotFoundError:
    import importlib_resources as resources
```

### Handle Missing Packages: Use an Alternative

```python
try:
    from quicktions import Fraction
except ModuleNotFoundError:
    from fractions import Fraction
```

### Handle Missing Packages: Use a Mock Instead

Create mock objects that serve as drop-in replacements for optional packages.

### Import Scripts as Modules

Use `if __name__ == "__main__":` to allow a file to work as both a script and a library:

```python
def main():
    ...

if __name__ == "__main__":
    main()
```

### Run Python Scripts From ZIP Files

Python can run scripts packaged into ZIP files using `__main__.py`. Use `zipapp` to streamline:

```bash
$ python -m zipapp population_quiz -m population_quiz:main
```

### Handle Cyclical Imports

Cyclical imports happen when two or more modules import each other. Python’s module cache partially handles this, but side effects at import time can cause issues. Solutions:
- Break the cycles
- Keep modules free of side effects at import time
- Do imports locally inside functions

### Profile Imports

Python 3.7+ supports `-X importtime` to measure import times:

```bash
$ python -X importtime -c "import datetime"
```

## Conclusion

**Key learnings:**
- Create namespace packages
- Import resources and data files
- Decide what to import dynamically at runtime
- Extend Python’s import system
- Handle different versions of packages

**Authoritative sources:**
- [The import system](https://docs.python.org/reference/import.html)
- [The `importlib` package](https://docs.python.org/library/importlib.html)
- [PEP 420: Implicit namespace packages](https://www.python.org/dev/peps/pep-0420/)
- [Importing modules](https://docs.python.org/library/modules.html)