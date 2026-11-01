# Python Imports Guide

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-01
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](/Users/simonlau/code/python05-bis/raw/python-programming/2026-11-01-the-codex-python05-bis.md)
> Updated: 2026-11-01

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

## Summary of Key Concepts

1. **Import Syntax**: Three main types (import, from import, import *)
2. **Import Paths**: Absolute vs relative imports
3. **Package Structure**: Role of __init__.py files
4. **Best Practices**: Import ordering, avoid wildcards
5. **Error Handling**: Common issues and solutions
6. **Testing**: Verify import structures work correctly

## See Also

- [Python Package Structure Basics](/wiki/python-programming/python-package-basics)
- [Environment Configuration](/wiki/python-programming/python-dotenv-usage)
- [Dependency Management](/wiki/python-programming/python-dependency-management)

## Status Notes

> **Status: Draft**
> This article covers Python import mechanisms as taught in Exercises 2 and 3 of The Codex. Content may be updated based on specific import requirements and exercise implementations.