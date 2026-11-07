# Python Package Structure Basics

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-01; Real Python (Charles de Villiers); 2025-07-09
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](../../raw/python-programming/2026-11-01-the-codex-python05-bis.md); [What Is Python's `__init__.py` For?](../../raw/python-programming/2026-11-07-realpython-python-init-py.md)
> Updated: 2026-11-07

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

## Regular Packages vs Namespace Packages

A directory **without an `__init__.py` file** becomes a **namespace package**, which behaves differently from a regular package and may cause slower imports. Since the adoption of **PEP 420** in Python 3.3, Python supports implicit namespace packages identified only by the absence of `__init__.py`.

| Aspect | Regular Package | Namespace Package |
|---|---|---|
| `__init__.py` | Present | Absent |
| Import speed | Faster (direct path) | Slower (searches whole `sys.path`) |
| Namespace scope | Single directory | Can span multiple directories |
| Name collisions | Detected at import time | Detected at runtime |

**Recommendation:** Unless you intentionally want a namespace package, include `__init__.py` in every package directory for more efficient and predictable imports.

## What Kind of Code Goes in `__init__.py`?

There’s no requirement to include any executable code inside `__init__.py`. It’s common to create an empty `__init__.py` file that serves only as a marker. However, `__init__.py` can also contain:

- **Import statements** (absolute or relative) to expose names from submodules
- **Variables and constants** at the package level
- **Functions and classes** defined at package level
- **Configuration or settings** for the package
- **Metadata** such as version number, author, project URL

Example with package metadata:

```python
# mediatools/__init__.py

__version__ = "0.1.0"
__author__ = "Python Alchemist"
```

## When Does `__init__.py` Get Executed?

An `__init__.py` file is executed **the first time its package is imported**. This happens when:

- You import the package explicitly (`import mediatools`)
- You import a module within the package (`from mediatools.audio import utils`)
- You import a subpackage or a module within a subpackage

Python maintains a cache of imported modules (`sys.modules`), so `__init__.py` code runs **only once** — even if you import the package multiple times. Subsequent imports reuse the cached module object.

You can force re-execution with `importlib.reload()`:

```python
import mediatools  # Executes mediatools/__init__.py once
import importlib
mediatools = importlib.reload(mediatools)  # Re-executes __init__.py
```

Use dynamic imports and reloading selectively — only when static imports don’t provide enough flexibility.

## Controlling What’s Exported From a Package

### Underscore Convention (Non-Public Names)

Names starting with one or more leading underscores are conventionally non-public. External code shouldn’t reference them, but Python doesn’t enforce this:

```python
>>> mediatools.audio.utils._secret_password
'Alakazam!'  # Accessible, but by convention shouldn't be used externally
```

### `__all__` Variable

Python provides a special `__all__` list that controls which names are imported by `from module import *`:

```python
# mediatools/graphics/utils.py

__all__ = ["solarize", "enhance"]
```

With this, `from mediatools.graphics.utils import *` imports only `solarize` and `enhance`, excluding `indiana_pi`.

`__all__` is also respected by documentation tools and IDE autocompletion tools when defining the code’s public API.

### Explicit Public API via `__init__.py`

You can define a simplified, coherent namespace by importing selected names into the package’s `__init__.py`:

```python
# mediatools/__init__.py

from .audio.utils import enhance as audio_enhance
from .audio.utils import wobbulate
from .graphics.utils import enhance as graphics_enhance
from .graphics.utils import solarize
```

This conforms to the software engineering principle of **information hiding** — the package user doesn’t need to see the internal details of subpackages:

```python
>>> from mediatools import wobbulate, solarize, audio_enhance, graphics_enhance
>>> wobbulate()
Wibble wobble
>>> audio_enhance()
Enhancing audio
```

## Importing Packages into `__init__.py` (Internal Use Only)

Sometimes you want to import modules into `__init__.py` for internal use without exposing them to package users. Prefix those names with underscores:

```python
from datetime import date as _date
from math import gcd as _gcd

def fancy_date_calculator() -> str:
    today = _date.today
    ...
    return "Calculated result"
```

User code sees only `fancy_date_calculator()` as public; `_date` and `_gcd` are clearly non-public.

## Top-Level `__init__.py` vs Subpackage `__init__.py`

The `__init__.py` at the top level of an import tree often contains extra metadata about the library as a whole — version number, project URL, developer contact information. Otherwise, it behaves the same as any other `__init__.py`.

You’d typically keep subpackage `__init__.py` files empty, though nothing prevents you from recording version information for subpackages as well.

## See Also

- [Python Imports Guide](/wiki/python-programming/python-imports-guide.md)
- [Virtual Environment Management](/wiki/python-programming/virtual-environment-management.md)
- [Dependency Management](/wiki/python-programming/python-dependency-management.md)
- [Python pip: Standard Package Manager](/wiki/python-programming/python-pip.md)
- [The Codex: Packages, Environments and the Alchemist's Toolchain](/wiki/python-programming/the-codex-packages-environments-and-alchemy-toolchain.md)

## Status Notes

> **Status: Draft**
> This article covers Python package structure fundamentals from The Codex (Exercise 2) and Real Python’s “What Is Python's `__init__.py` For?” tutorial. It includes `__init__.py` as package marker, namespace packages vs regular packages, execution timing and caching, `__all__` variable, underscore conventions for non-public names, explicit public API via `__init__.py` imports, and top-level `__init__.py` metadata.