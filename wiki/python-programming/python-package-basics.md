# Python Package Structure Basics

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-01
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](/Users/simonlau/code/python05-bis/raw/python-programming/2026-11-01-the-codex-python05-bis.md)
> Updated: 2026-11-01

## Overview

Python package structure is fundamental to creating organized, reusable, and maintainable code. A package is a collection of related modules organized in a directory hierarchy, distinguished from regular directories by the presence of an `__init__.py` file. This structure allows for proper code organization and controlled API exposure.

## Package Architecture

**Core Components:**
- **Package Directory**: Directory containing related Python modules
- **`__init__.py`**: Special file that makes a directory a Python package and controls API exposure
- **Modules**: Individual `.py` files containing code
- **Subpackages**: Nested packages for hierarchical organization

## `__init__.py` Functions

The `__init__.py` file serves multiple critical purposes:

1. **Package Recognition**: Tells Python this is a package directory
2. **API Control**: Controls what gets imported when `from package import *` is used
3. **Initialization Code**: Can contain setup code that runs when the package is imported
4. **Namespace Management**: Organizes related functionality into logical groups

## Exposure Control Examples

### Controlling Package API
```python
# alchemy/__init__.py

# Expose these functions at package level
from .elements import create_fire
from .elements import create_water

# Hide these functions (not exposed at package level)
# from .elements import create_earth  # This stays hidden
# from .elements import create_air   # This stays hidden
```

### Creating Subpackages
```python
# alchemy/transmutation/__init__.py

# Expose transmutation functions
from .recipes import lead_to_gold

# Hide implementation details
# from .recipes import complex_transmutation_logic  # Hidden
```

## Common Patterns

### 1. Minimal Package Structure
```python
alchemy/
    __init__.py          # Package gateway
    elements.py          # Core element definitions
    potions.py           # Element combinations
    transmutation/
        __init__.py      # Subpackage gateway
        recipes.py       # Complex transformations
```

### 2. Multi-level Package Hierarchy
```python
myproject/
    __init__.py          # Main package
    core/
        __init__.py      # Core subpackage
        utilities.py
    services/
        __init__.py      # Services subpackage
        api.py
    tests/
        __init__.py      # Testing subpackage
        unit/
        integration/
```

## Best Practices

### 1. Selective API Exposure
Use `__init__.py` to expose only intended functionality:

```python
# Expose frequently used functions
__all__ = ['create_fire', 'create_water', 'healing_potion']

# Hide implementation details
# create_earth = create_earth()  # Not exposed at package level
```

### 2. Version Information
Store package version in `__init__.py`:

```python
# alchemy/__init__.py

__version__ = "1.0.0"
__author__ = "Python Alchemist"
```

### 3. Package-level Configuration
Place common configuration in `__init__.py`:

```python
# alchemy/__init__.py

DEFAULT_ELEMENTS = ["earth", "air", "fire", "water"]
MAX_POTION_INGREDIENTS = 3

# This becomes: alchemy.DEFAULT_ELEMENTS
```

## Import Mechanisms

### Package Import Options

1. **Full Package Import**: `import alchemy`
2. **Function from Package**: `from alchemy import create_fire`
3. **Module from Package**: `from alchemy import elements`
4. **Subpackage Access**: `from alchemy.transmutation import lead_to_gold`

### Import Path Examples

```python
# Direct module access
import alchemy.elements
from alchemy import elements

# Subpackage access  
from alchemy.transmutation import recipes
import alchemy.transmutation.recipes

# Selective function import
from alchemy import create_fire, create_water
from alchemy.elements import create_fire
```

## Exercise-Specific Applications

### Exercise 2: The Alembic
- **Goal**: Demonstrate package exposure control
- **Key Concept**: `alchemy/__init__.py` exposes `create_air` but hides `create_earth`
- **Learning Outcome**: Understanding how `__init__.py` controls API access

### Exercise 3: Distillation and Transmutation
- **Goal**: Master nested import mechanisms
- **Key Concept**: Multiple import styles for different use cases
- **Learning Outcome**: When to use absolute vs relative imports

## See Also

- [Python Imports Guide](/wiki/python-programming/python-imports-guide)
- [Virtual Environments](/wiki/python-programming/virtual-environments)
- [Dependency Management](/wiki/python-programming/python-dependency-management)

## Status Notes

> **Status: Draft**
> This article establishes the foundational package structure concepts covered in Exercise 2 of The Codex. May be updated based on specific exercise requirements and additional learning materials.