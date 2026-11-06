# Circular Dependency Management

> Sources: The Codex - Python Module 05 BIS - Course material; 2026-11-02
> Raw: [The Codex: Packages, Environments and the Alchemist's Toolchain](/Users/simonlau/code/python05-bis/raw/python-programming/2026-11-01-the-codex-python05-bis.md)
> Updated: 2026-11-02

## Overview

Circular dependencies occur when two or more modules depend on each other, directly or indirectly, creating an import cycle that prevents Python from initializing either module properly. The Codex refers to this as "The final mystery, and the one that destroys laboratories."

A circular dependency happens when:
- Module A imports Module B at the top level
- Module B imports Module A at the top level
- Neither module can fully initialize because each waits for the other

## The Problem: Import Cycles

### Naive Circular Dependency

When two modules import each other at the module level, Python cannot fully initialize either:

```
dark_spellbook.py imports dark_validator.py
dark_validator.py imports dark_spellbook.py
```

**Error:**
```
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'dark_spellbook'
```

The traceback shows:
1. `dark_spellbook.py` line 2: `from .dark_validator import validate_ingredients`
2. `dark_validator.py` line 2: `from .dark_spellbook import dark_spell_allowed_ingredients`
3. Python cannot complete either import → ImportError

### Why Circular Imports Fail

Python imports modules by:
1. Finding the module file
2. Executing the module code top-to-bottom
3. Binding names in the module's namespace
4. Making the module available to other importers

When Module A imports Module B, Python starts executing Module B. If Module B then imports Module A, Python finds Module A is already being imported (partially initialized) and cannot provide the names Module B needs.

## The Two Grimoires: Light vs Dark

The Codex presents the same feature twice to demonstrate the difference:

### The Light Grimoire (which survives)

The light grimoire uses a design decision that avoids circular dependency:

```python
# alchemy/grimoire/light_spellbook.py
ALLOWED_INGREDIENTS = ["earth", "air", "fire", "water"]

def light_spell_allowed_ingredients():
    return ALLOWED_INGREDIENTS

def light_spell_record(spell_name: str, ingredients: str):
    from .light_validator import validate_ingredients  # Local import
    return validate_ingredients(ingredients)

# alchemy/grimoire/light_validator.py
def validate_ingredients(ingredients: str):
    from .light_spellbook import light_spell_allowed_ingredients  # Local import
    allowed = light_spell_allowed_ingredients()
    if any(ing in ingredients.lower() for ing in allowed):
        return f"{ingredients} VALID"
    return f"{ingredients} INVALID"
```

**Key Design Decision:** Imports are placed inside functions (local imports), not at module level. This defers the circular dependency until both modules are fully initialized.

**Result:**
```
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

### The Dark Grimoire (which does not survive)

The dark grimoire uses naive top-level imports:

```python
# alchemy/grimoire/dark_spellbook.py
from .dark_validator import validate_ingredients  # Top-level import

DARK_INGREDIENTS = ["bats", "frogs", "arsenic", "eyeball"]

def dark_spell_allowed_ingredients():
    return DARK_INGREDIENTS

def dark_spell_record(spell_name: str, ingredients: str):
    return validate_ingredients(ingredients)

# alchemy/grimoire/dark_validator.py
from .dark_spellbook import dark_spell_allowed_ingredients  # Top-level import

def validate_ingredients(ingredients: str):
    allowed = dark_spell_allowed_ingredients()
    ...
```

**Key Design Decision:** Top-level mutual imports create an unresolvable cycle.

**Result:**
```
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'dark_spellbook'
```

## Exercise 4: Avoid the Explosion

**Objective:** Write the same feature twice — once working, once broken — to demonstrate that the difference between success and failure is a single design decision, not a single line of syntax.

### Light Grimoire Files

**`alchemy/grimoire/light_spellbook.py`:**
- `light_spell_allowed_ingredients()` → returns `["earth", "air", "fire", "water"]`
- `light_spell_record(spell_name: str, ingredients: str)` → returns whether spell was recorded or rejected (decision comes from validator)

**`alchemy/grimoire/light_validator.py`:**
- `validate_ingredients(ingredients: str)` → returns string containing ingredients and "VALID" or "INVALID" keyword

**Validation Rule:** Ingredients are valid if they include at least one of the ingredients allowed by the spellbook (case insensitive).

**Test:** `ft_kaboom_0.py` accesses the grimoire package and records a light spell flawlessly.

### Dark Grimoire Files

**`alchemy/grimoire/dark_spellbook.py`:**
- Dark counterparts with `dark_`-prefixed function names
- Dark ingredients: `["bats", "frogs", "arsenic", "eyeball"]`

**`alchemy/grimoire/dark_validator.py`:**
- Dark validator counterpart

**Test:** `ft_kaboom_1.py` reaches `dark_spellbook.py` directly and tries to record a dark spell — must fail and raise an exception.

## Circular Dependency Solutions

### Solution 1: Local Imports (Function-Level Imports)

Move imports inside functions so they execute after both modules are initialized:

```python
# Module A
def function_a():
    from module_b import function_b  # Local import
    return function_b()
```

**When to use:** Simple cases where the circular import is only needed in specific functions.

### Solution 2: Restructure Code

Move shared functionality to a third module:

```python
# Instead of:
# module_a imports module_b
# module_b imports module_a

# Do:
# module_a imports module_c
# module_b imports module_c
# module_c contains shared functionality
```

**When to use:** When two modules share common logic that can be extracted.

### Solution 3: Refactor API Design

Change the dependency direction so one module doesn't need to import the other:

```python
# Module A calls Module B's function
# Module B does NOT call Module A's function
# Module A passes data to Module B instead
```

**When to use:** When one module can be made independent of the other.

### Solution 4: Use Import Inside Function (Deferred Import)

```python
# Module A
def function_a():
    import module_b  # Import deferred until function call
    return module_b.function_b()
```

**When to use:** When the circular import is only needed at runtime, not at module definition time.

### Solution 5: TYPE_CHECKING for Type Hints

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module_b import ClassB  # Only imported for type checkers

def function_a(param: "ClassB"):
    pass  # Actual import deferred
```

**When to use:** For type hints in circular dependency scenarios.

## Exercise-Specific Application

### ft_kaboom_0.py (Light Grimoire - Working)

```python
# ft_kaboom_0.py accesses the grimoire package
from alchemy.grimoire import light_spell_record

result = light_spell_record("Fantasy", "Earth, wind and fire")
print(f"Spell recorded: {result}")
```

Expected output:
```
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

### ft_kaboom_1.py (Dark Grimoire - Broken)

```python
# ft_kaboom_1.py reaches dark_spellbook.py directly
from alchemy.grimoire.dark_spellbook import dark_spell_record

result = dark_spell_record("Dark Ritual", "bats, frogs, arsenic")
print(result)
```

Expected output:
```
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'dark_spellbook'
```

## Common Causes of Circular Dependencies

| Cause | Example | Solution |
|-------|---------|----------|
| Mutual top-level imports | A imports B, B imports A | Local imports or restructure |
| Shared constants | Both modules need same constants | Extract to third module |
| Type hints | A uses B's type in annotations | TYPE_CHECKING guard |
| Factory functions | A creates B, B creates A | Pass instances instead |
| Plugin systems | Plugin imports host, host imports plugin | Use abstract base classes |

## Prevention Strategies

### 1. Design for One-Way Dependencies

```
Module A → Module B → Module C
          ↑           ↓
          └───────────┘  ← Back-reference avoided
```

### 2. Extract Shared Code

```
Module A → Module C (shared)
Module B → Module C (shared)
```

### 3. Use Dependency Injection

```python
# Instead of Module A importing Module B
class ModuleA:
    def __init__(self, validator):
        self.validator = validator  # Injected, not imported
```

### 4. Defer Imports

```python
def function():
    from module_b import function_b  # Deferred until call time
    return function_b()
```

## See Also

- [Python Package Structure Basics](/wiki/python-programming/python-package-basics)
- [Python Imports Guide](/wiki/python-programming/python-imports-guide)

## Status Notes

> **Status: Draft**
> This article covers circular dependency concepts as taught in Exercise 4 of The Codex. Content may be refined based on specific implementation requirements.