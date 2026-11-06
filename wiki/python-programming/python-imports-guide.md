# Python Imports Guide

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-01; Real Python (Geir Arne Hjelle); 2020-07-08
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](../../raw/python-programming/2026-11-01-the-codex-python05-bis.md); [Python import: Advanced Techniques and Tips](../../raw/python-programming/2026-11-06-realpython-python-import.md)
> Updated: 2026-11-06

## Overview

Python imports are fundamental to code organization, reuse, and modularity. Imports allow modules to access functionality from other modules, creating a hierarchical structure that supports both large-scale applications and simple scripts. The import system in Python provides several mechanisms for accessing code, each with specific use cases and best practices.

## Import Mechanisms

### 1. Standard Import

**Syntax:** `import module_name`

```python
import os
import sys
import math
```

**Usage:**
```python
# Access module attributes
print(os.path.join("dir", "file.txt"))
print(math.sqrt(16))

# Module is available throughout the code
```

**Best Practices:**
- Use for modules accessed multiple times
- Good for organizing related functionality
- Can rename imported modules: `import os as operating_system`

### 2. From Import

**Syntax:** `from module_name import specific_function`

```python
from os import path, getenv
from math import sqrt, pi
```

**Usage:**
```python
# Directly access imported functions
print(path.join("dir", "file.txt"))
print(sqrt(16), pi)
```

**Best Practices:**
- Use when you need specific functions from a module
- Reduces verbosity when using only a few module features
- Can import multiple functions: `from os import path, getenv, environ`

### 3. Import All

**Syntax:** `from module_name import *`

```python
from os import *
```

**Usage:**
```python
# All public functions from module become available
print(join("dir", "file.txt"))  # path.join
print(getenv("HOME"))  # getenv
```

**Best Practices:**
- Use cautiously - can lead to namespace pollution
- Generally discouraged in production code
- Use only when you explicitly understand what's being imported

## Exercise-Specific Import Examples

### Exercise 2: The Alembic

**Using import... structure:**
```python
# ft_alembic_0.py - access elements.py at root
import ...elements
print(...elements.create_fire())  # Fire element created
```

**Using import alchemy:**
```python
# ft_alembic_1.py - go through package interface
import alchemy
print(alchemy.create_air())  # Air element created

# This fails because create_earth is hidden
# print(alchemy.create_earth())  # AttributeError
```

### Exercise 3: Distillation and Transmutation

**Using from... import... structure:**
```python
# ft_distillation_0.py - direct access to potions.py
from ...alchemy import potions
print(potions.healing_potion())
```

**Using import alchemy.transmutation.recipes:**
```python
# ft_transmutation_0.py - use import... structure
import ...alchemy.transmutation.recipes
print(...alchemy.transmutation.recipes.lead_to_gold())
```

## Absolute vs Relative Imports

### Absolute Imports

**Syntax:** `import package.subpackage.module`

**When to Use:**
- When the module can be found in the Python path
- When importing from the main application
- When the relationship between packages is clear

**Example:**
```python
import os.path  # Absolute import
import alchemy.elements  # Import from package
```

### Relative Imports

**Syntax:** `from . import module` or `from .subpackage import module`

**When to Use:**
- When importing within a package
- When the module is part of a subpackage
- When working with sibling modules

**Example:**
```python
# Within alchemy/transmutation/recipes.py
from ..elements import create_fire  # Import from parent package
from . import potions  # Import from same package
from .recipes import lead_to_gold  # Import from same package
```

## Package Structure and Imports

### 1. Single Module Structure

```python
myproject/
    elements.py          # Single module
    ft_alembic_0.py       # Uses: import ...elements
    ft_alembic_1.py       # Uses: import alchemy
```

### 2. Package with __init__.py

```python
alchemy/
    __init__.py          # Package gateway
    elements.py          # Core functionality
    potions.py           # Element combinations
    transmutation/
        __init__.py      # Subpackage
        recipes.py       # Complex transformations
```

### 3. Import Paths Examples

**From alchemy/elements.py:**
```python
# Import from parent
from .. import alchemy

# Import from sibling
from ..potions import healing_potion

# Import from same package
from . import elements

# Import specific function
from ..elements import create_fire
```

## Common Import Patterns

### 1. Pyramid Structure

```python
alchemy/
    __init__.py
    elements.py
    potions.py
    transmutation/
        __init__.py
        recipes.py
```

**Import patterns:**
```python
# From root level
import alchemy.elements
from alchemy import elements

# From within alchemy
from . import elements
from .elements import create_fire

# From within transmutation
from .. import alchemy
from ...elements import create_fire
from .recipes import lead_to_gold
```

### 2. Flat Structure

```python
myproject/
    elements.py
    potions.py
    transmutation.py
    recipes.py
```

**Import patterns:**
```python
import elements
from elements import create_fire
import transmutation.recipes
```

## Import Best Practices

### 1. Import Order

```python
# 1. Standard library imports
import os
import sys
import math

# 2. Third-party imports
import requests
import pandas as pd

# 3. Local application imports
from . import elements
from ..alchemy import potions
```

### 2. Avoid Wildcard Imports

```python
# Bad practice
from os import *

# Good practice
from os import path, getenv
```

### 3. Use Meaningful Aliases

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

### 4. Import Structure Clarity

```python
# Clear and explicit
from alchemy.elements import create_fire, create_water
from alchemy.potions import healing_potion, strength_potion

# Obscure and potentially confusing
from alchemy import *
```

## Common Import Errors and Solutions

### 1. ModuleNotFoundError

**Problem:** Module cannot be found
**Solutions:**
- Check if the module exists
- Ensure the module is in the Python path
- Use absolute imports when working across packages

```python
# Before (might fail)
from .elements import create_fire

# After (more robust)
from ..elements import create_fire
```

### 2. Circular Import Errors

**Problem:** Module A imports Module B, and Module B imports Module A
**Solutions:**
- Restructure imports
- Use function-level imports
- Import inside functions/methods

```python
# Problematic structure
alchemy/
    __init__.py
    elements.py  # imports from __init__.py
    potions.py   # imports from elements.py

# Better structure
alchemy/
    __init__.py  # minimal - only essential exports
    elements.py  # imports from separate modules
    potions.py   # imports from separate modules
```

### 3. Import Outside Function Context

**Problem:** Importing at module level when conditional import is needed
**Solution:** Import inside functions

```python
def some_function():
    import heavy_module  # Import only when function is called
    return heavy_module.do_something()
```

## Testing Import Structures

### 1. Test Import Paths

```python
import pytest
import sys

def test_alchemy_import():
    import alchemy.elements
    from alchemy.elements import create_fire
    
    assert alchemy.create_fire() == "Fire element created"
    assert create_fire() == "Fire element created"

def test_relative_import():
    from alchemy.transmutation import recipes
    assert recipes.lead_to_gold() == "Recipe transmuting Lead to Gold"
```

### 2. Test Import Scenarios

```python
def test_import_from_root():
    """Test importing from root level"""
    import elements
    assert elements.create_fire() == "Fire element created"

def test_import_from_package():
    """Test importing from package"""
    from alchemy.elements import create_fire
    assert create_fire() == "Fire element created"

def test_import_from_subpackage():
    """Test importing from subpackage"""
    from alchemy.transmutation.recipes import lead_to_gold
    assert lead_to_gold() == "Recipe transmuting Lead to Gold"
```

## Namespace Packages

Namespace packages have been available since Python 3.3. They’re less dependent on the underlying file hierarchy and can be split across multiple directories. A namespace package is created automatically if you have a directory containing a `.py` file but no `__init__.py`. See PEP 420.

Unlike regular packages, namespace packages cannot use `__init__.py` files. They are useful when you want to add your own modules to an existing package without modifying the original package.

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
    with resources.open_text(
        "data", "WPP2019_TotalPopulationBySex.csv"
    ) as fid:
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

`sys.modules` acts as a module cache — it contains references to all modules that have been imported. The first place Python looks for modules is `sys.modules`. If a module is already available, it isn’t loaded again.

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

`reload()` requires a module object, not a string like `import_module()` does.

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

Create mock objects that serve as drop-in replacements for optional packages:

```python
try:
    from colorama import init, Back, Cursor, Fore, Style
except ModuleNotFoundError:
    from collections import UserString

    class ColoramaMock(UserString):
        def __call__(self, *args, **kwargs):
            return self
        def __getattr__(self, key):
            return self

    init = ColoramaMock("")
    Back = Cursor = Fore = Style = ColoramaMock("")
```

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

1. **Break the cycles** — restructure your architecture
2. **Keep modules free of side effects at import time** — define only attributes, functions, classes
3. **Do imports locally inside functions** — defer the import until after both modules are fully loaded

```python
# yin.py
number = 42

def combine():
    import yang
    return number + yang.number
```

### Profile Imports

Python 3.7+ supports `-X importtime` to measure import times:

```bash
$ python -X importtime -c "import datetime"
```

This helps identify slow imports and optimize startup time.

## Summary of Key Concepts

1. **Import Syntax**: Three main types (import, from import, import *)
2. **Import Paths**: Absolute vs relative imports
3. **Package Structure**: Role of `__init__.py` files; namespace packages (PEP 420)
4. **Best Practices**: Import ordering, avoid wildcards, prefer absolute imports
5. **Error Handling**: ModuleNotFoundError, circular imports
6. **Testing**: Verify import structures work correctly
7. **Resource Imports**: `importlib.resources` for package data files
8. **Dynamic Imports**: `importlib.import_module()` for runtime imports
9. **Import Internals**: `sys.modules` cache, `sys.meta_path` finders
10. **Profiling**: `python -X importtime` to measure import times

## See Also

- [Python Package Structure Basics](/wiki/python-programming/python-package-basics.md)
- [Python Dotenv Usage](/wiki/python-programming/python-dotenv-usage.md)
- [Python Dependency Management](/wiki/python-programming/python-dependency-management.md)
- [Python pip: Standard Package Manager](/wiki/python-programming/python-pip.md)
- [Python uv: All-in-One Package and Project Manager](/wiki/python-programming/python-uv.md)
- [Virtual Environment Management](/wiki/python-programming/virtual-environment-management.md)
- [The Codex: Packages, Environments and the Alchemist's Toolchain](/wiki/python-programming/the-codex-packages-environments-and-alchemy-toolchain.md)

## Status Notes

> **Status: Draft**
> This article covers Python import mechanisms as taught in Exercises 2 and 3 of The Codex, plus advanced topics from Real Python’s “Python import: Advanced Techniques and Tips” tutorial including namespace packages, resource imports, dynamic imports, import system internals, finders and loaders, reloading modules, cyclical imports, and import profiling.
