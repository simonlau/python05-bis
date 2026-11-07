# What Is Python's `__init__.py` For?

> Source: https://realpython.com/python-init-py/
> Collected: 2026-11-07
> Published: 2025-07-09

# What Is Python's `__init__.py` For?

by Charles de Villiers Updated Jul 09, 2025 Reading time estimate 23m

## Table of Contents

- In Short: `__init__.py` Declares a Folder as a Regular Python Package
- What Happens When I Add Code to `__init__.py`?
- What Happens if I Don’t Add an `__init__.py` File?
- What Kind of Code Should I Put in `__init__.py`?
- When Does `__init__.py` Get Executed?
- How Is `__init__.py` Used in a Practical Example?
- Can I Use `__init__.py` to Control What’s Exported From a Package?
- Is a Top-Level `__init__.py` Different From One in a Subpackage?
- Conclusion
- Frequently Asked Questions

## Introduction

Python’s special `__init__.py` file marks a directory as a regular Python package and allows you to import its modules. This file runs automatically the first time you import its containing package. You can use it to initialize package-level variables, define functions or classes, and structure the package’s namespace clearly for users.

**By the end of this tutorial, you’ll understand that:**

- A directory **without an `__init__.py` file** becomes a **namespace package**, which behaves differently from a regular package and may cause slower imports.

- You can use `__init__.py` to explicitly define a package’s **public API** by importing specific modules or functions into the package namespace.

- The Python convention of using **leading underscores** helps indicate to users which objects are intended as **non-public**, although this convention can still be bypassed.

- Code inside `__init__.py` runs **only once** during the first import, even if you run the import statement multiple times.

Understanding how to effectively use `__init__.py` helps you structure your Python packages in a clear, maintainable way, improving usability and namespace management.

**Note:** The filename `__init__.py` is hard to pronounce. Most people find it easier to call it *dunder-init*.

## In Short: `__init__.py` Declares a Folder as a Regular Python Package

The special file `__init__.py` serves as a marker to indicate that its containing directory is a regular package. When people talk about a **package** in Python, they generally mean a regular package. The `__init__.py` file is a Python source file, which means that it’s also a module.

### Module vs Package in Python

|  | Module | Package |
|---|---|---|
| **Definition** | A single Python file containing code | A directory containing one or more Python modules |
| **Naming** | The filename without the `.py` extension | The directory name |
| **Contents** | Functions, classes, and variables | Modules and optionally subpackages |
| **Purpose** | Organizing small projects, simple code reuse | Organizing large projects, code reuse |
| **Importing** | Import directly (`import module`) | Import package or its modules (`import package.module`) |

The existence of `__init__.py` makes the Python loader identify its containing directory as a regular package. This means you can import the whole directory, specific modules within it, or even individual functions, variables, and classes from those modules using the package name.

You can also import those code objects into other modules, which allows your code to be reused in many flexible ways.

As mentioned, `__init__.py` may be an empty file, in which case it serves only to identify a package.

## What Happens When I Add Code to `__init__.py`?

If `__init__.py` does contain code, then that code will be executed when the package is first imported.

The code in `__init__.py` can perform a variety of useful tasks. For example, it can import other modules or packages and define its own functions or data. When a package is imported, all of its own code, along with everything it has itself imported, becomes accessible to the importing module.

### Example: Package with Variables

```
tools_project/
│
└── tools/
    └── __init__.py
```

**tools/__init__.py:**
```python
__version__ = "1.0.0"
magic_number = 42
```

```python
>>> import tools
>>> tools.__version__
'1.0.0'
>>> tools.magic_number
42
```

When you executed `import tools` in line 1, the `__init__.py` file in the `tools` directory was implicitly executed. That made the names in `tools/__init__.py` accessible via the `tools` prefix.

**Note:** The code in `__init__.py` is executed only once, even if you import the package multiple times.

## What Happens if I Don’t Add an `__init__.py` File?

So far, you’ve been learning about regular packages, but Python also supports packages of another type, known as **namespace packages**. A namespace package doesn’t have an `__init__.py` file. You can still import it, provided Python can find it through `sys.path`.

Both regular packages and namespace packages define namespaces. The difference lies in the fact that a namespace package isn’t limited to a single directory—it’s the namespace prefix, not the physical directory, that identifies the package contents.

**Note:** Namespace packages have been around for many years, but they used to require some extra setup. Since the adoption of **PEP 420** in Python 3.3, the language has had *implicit* namespace packages, identified only by the absence of `__init__.py`. This makes them easier to create intentionally, but also easier to create by accident!

### Example: Namespace Package

```
tools_project/
│
├── tools/
│   └── __init__.py
│
└── tools_ns/
```

```python
>>> import tools
>>> tools.__path__
['/tools_project/tools']

>>> import tools_ns
>>> tools_ns.__path__
_NamespacePath(['/tools_project/tools_ns'])
```

Python finds `tools_ns` in the current directory, notes that it has no `__init__.py` within it, and imports it as a namespace package.

Namespace packages are useful for combining multiple codebases into a unified naming structure. For example, a corporation with a number of development sites might want to combine their various contributions under a single namespace.

However, namespace packages come with caveats:

1. **Slower imports** — when importing a namespace package, the interpreter must search the whole `sys.path` to ensure that it has found all the files contributing to the namespace.

2. **Name collisions aren’t detected until runtime** — because the full namespace can only be assembled at runtime.

Unless you’re sure that you want to build a namespace package, you should opt for regular packages by including an `__init__.py` file within each package in your project. This will result in more efficient and predictable imports.

## What Kind of Code Should I Put in `__init__.py`?

There’s no requirement to include any executable code inside `__init__.py`. As you’ve already learned, it’s common to create an empty `__init__.py` file in a directory, where it serves as a marker to indicate that the directory should be treated as a regular package.

However, `__init__.py` can also contain functions, classes, data, and absolute or relative import statements.

This can be useful for importing names from submodules to structure a sensible namespace for users of the top-level package. Any names you import into the package become part of its top-level namespace and can then be more conveniently referenced by client code.

`__init__.py` is a good place to define utility functions, constants, and variables that apply to the whole package.

You can use the `__init__.py` file to:

- Import other modules that are needed by code within `__init__.py` itself
- Define variables or functions at the package level
- Set up configuration or settings for the package
- Include documentation or define metadata for the package
- Provide a simplified, coherent namespace for package users

## When Does `__init__.py` Get Executed?

An `__init__.py` file is executed the first time its package is imported. This will happen:

- If you import the package explicitly
- If you import a module within the package
- If you import a subpackage of the package, or a module within that subpackage

The `__init__.py` file starts executing as soon as the interpreter encounters the corresponding `import` statement. Any nested imports within the file will also be executed as they’re encountered.

Python maintains a cache of imported modules (`sys.modules`), so you can’t import the same module twice using a normal `import` statement. Python silently skips the second `import` statement, and the contents of `__init__.py` won’t be re-executed.

## How Is `__init__.py` Used in a Practical Example?

Suppose you’re starting a new project called `media_project`, with its own root directory. Below that, a directory named `mediatools` contains its own `__init__.py`, defining the `mediatools` package and namespace. Within that package, you might include subpackages named `audio` and `graphics`.

### Project Layout

```
media_project/
│
└── mediatools/
    │
    ├── audio/
    │   ├── __init__.py
    │   └── utils.py
    │
    ├── graphics/
    │   ├── __init__.py
    │   └── utils.py
    │
    └── __init__.py
```

### mediatools/audio/utils.py

```python
print(f"Importing {__name__}")

def wobbulate():
    print("Wibble wobble")

def enhance():
    print("Enhancing audio")

_secret_password = "Alakazam!"
__top_secret_password = "!mazakalA"
```

### mediatools/graphics/utils.py

```python
print(f"Importing {__name__}")

def solarize():
    print("Solarizing")

def enhance():
    print("Enhancing graphics")

indiana_pi = 3.2
```

### mediatools/__init__.py

```python
print(f"Importing {__name__}")
```

### mediatools/audio/__init__.py

```python
print(f"Importing {__name__}")
```

### mediatools/graphics/__init__.py

```python
print(f"Importing {__name__}")
```

### Import Behavior

```python
>>> from mediatools.audio import utils as audio_utils
Importing mediatools
Importing mediatools.audio
Importing mediatools.audio.utils

>>> from mediatools.graphics import utils as graphics_utils
Importing mediatools.graphics
Importing mediatools.graphics.utils

>>> audio_utils.wobbulate()
Wibble wobble

>>> graphics_utils.solarize()
Solarizing

>>> graphics_utils.indiana_pi
3.2
```

Even though your `import` statements explicitly mentioned only the two `utils` modules, the code in `mediatools.__init__.py`, `mediatools.audio.__init__.py`, and `mediatools.audio.utils` was implicitly executed.

Notice that the code in `mediatools.__init__.py` was executed only once, even though `mediatools` is a parent package of both the imported modules.

The second import of the same module doesn’t execute any imports:

```python
>>> from mediatools.audio import utils

>>> from mediatools.audio import utils as more_utils

>>> utils.enhance()
Enhancing audio

>>> more_utils.enhance()
Enhancing audio
```

You can force re-execution of an `__init__.py` file with a dynamic import using Python’s `importlib` library:

```python
>>> import mediatools
Importing mediatools

>>> import importlib

>>> mediatools = importlib.reload(mediatools)
Importing mediatools
```

However, keep in mind that you should use dynamic imports and reloading selectively—only when Python’s standard, static imports don’t provide enough flexibility or when you explicitly need runtime control over modules.

## Can I Use `__init__.py` to Control What’s Exported From a Package?

The short answer is this: not really. Python does have mechanisms and conventions to control exports, but they’re easily circumvented.

### Underscore Convention

One such convention concerns names that start with one or more leading underscores. The convention dictates that external code shouldn’t reference these names. By using these “underscore names,” the package developer can help the package user to understand what should and shouldn’t be included in the public API.

In practice, it’s the package developer’s responsibility to use this convention to indicate the things that aren’t intended for export, but it’s up to the package user to respect the convention. It can easily be ignored:

```python
>>> import mediatools.audio.utils

>>> mediatools.audio.utils._secret_password
'Alakazam!'

>>> mediatools.audio.utils.__top_secret_password
'!mazakalA'
```

Python is happy to import and print the values of these supposedly non-public variables.

### `import *` Syntax

The `import *` syntax does respect the underscore convention:

```python
>>> from mediatools.audio.utils import *

>>> _secret_password
Traceback (most recent call last):
  ...
NameError: name '_secret_password' is not defined

>>> __top_secret_password
Traceback (most recent call last):
  ...
NameError: name '__top_secret_password' is not defined
```

With this syntax, most of the names inside `mediatools.audio.utils` become available to your program without the prefix, but the underscore variables aren’t imported.

**Note:** The `import *` syntax is often convenient in interactive work, but it’s considered bad practice in larger projects because it erases the module namespace information. All the objects defined in `mediatools.audio.utils`—except those that start with an underscore—are imported and lose their prefix in the process. They become part of the global namespace, increasing the risk of name collisions.

### `__all__` Variable

Python provides a special list named `__all__` that, when defined in a module, controls which names are imported by a `from module import *` statement. Only the names listed in `__all__` will be imported.

Add to `mediatools/graphics/utils.py`:

```python
# ...

__all__ = ["solarize", "enhance"]
```

With this addition, `import *` will import only the two named functions, and `indiana_pi` is no longer visible:

```python
>>> from mediatools.graphics.utils import *

>>> indiana_pi
Traceback (most recent call last):
  ...
NameError: name 'indiana_pi' is not defined
```

Although you can’t prohibit your package’s users from importing symbols in a way you didn’t intend, you can structure your namespace in a way that helps them understand how the code is meant to work.

For example, instead of expecting a developer to dig into the details of the two `utils` packages to decide what to import and how to import it, you can add a couple of lines to `mediatools/__init__.py`:

```python
from .audio.utils import enhance as audio_enhance
from .audio.utils import wobbulate
from .graphics.utils import enhance as graphics_enhance
from .graphics.utils import solarize
```

Here you’ve used relative imports to simplify the developer’s view of the `mediatools` package. This conforms to the software engineering principle of *information hiding*: the package user doesn’t need to see the gory details of `mediatools` and its subpackages. They simply need an interface definition to help them use the package at a high level.

Now the user code can take advantage of the new interface:

```python
>>> from mediatools import (
...     wobbulate,
...     solarize,
...     audio_enhance,
...     graphics_enhance
... )

>>> wobbulate()
Wibble wobble

>>> solarize()
Solarizing

>>> audio_enhance()
Enhancing audio

>>> graphics_enhance()
Enhancing graphics
```

Using this interface, client code is better decoupled from the internals of the `mediatools` packages. This makes the client code easier to write and easier to maintain.

Sometimes, you want to import packages into `__init__.py` for its internal use, but to avoid polluting the namespace, you don’t want to expose those names to the users of your package:

```python
from datetime import date as _date
from math import gcd as _gcd
from some.thirdparty.dateutils import lunar_month as _lunar_month

def fancy_date_calculator() -> str:
    today = _date.today
    ...
    return "Calculated result"
```

When user code imports this package, it will see only one public function: `fancy_date_calculator()`. All the other symbols will be prefixed with underscores, making it clear that they’re not intended for public use.

### `__all__` is also respected by documentation tools

`__all__` is respected by documentation tools when defining the code’s public API. IDE autocompletion tools also check `__all__` to ensure that only public code completions are suggested.

## Is a Top-Level `__init__.py` Different From One in a Subpackage?

The `__init__.py` in the folder at the top level of an import tree often contains some extra metadata about the library as a whole. This can include its version number, the URL of its project site, and contact information for the developers. Otherwise, it behaves in the same way as any other `__init__.py`.

For example, say you want to add a package version number. A good spot for that would be inside of `mediatools/__init__.py`:

```python
__version__ = "0.1.0"

# ...
```

You’d likely keep the other `__init__.py` files empty, although nothing prevents you from recording version information for your subpackages there as well.

## Conclusion

In this tutorial, you’ve learned about the special role of Python’s `__init__.py` file in defining regular packages and distinguishing them from namespace packages.

**Key learnings:**

- Mark directories as **regular packages** using `__init__.py`
- Define a clear, explicit **public API** using imports in `__init__.py`
- Use **underscore prefixes** to indicate non-public symbols
- Control what’s imported with the **`__all__` variable**
- Understand when and how Python **executes code** in `__init__.py`

Effectively using `__init__.py` can help you create well-organized, maintainable, and intuitive packages. By structuring your packages properly, you improve readability, encourage reusability, and simplify package-level initialization.

## Frequently Asked Questions

**What does an empty `__init__.py` file do?**
An empty `__init__.py` file indicates to Python that the directory is a regular package, allowing you to import modules from it.

**What happens if you omit the `__init__.py` file from a package directory?**
Without `__init__.py`, Python recognizes the directory as a namespace package instead of a regular package. Namespace packages can span multiple directories, but their imports are usually slower.

**Can you control what gets imported from a package using `__init__.py`?**
You can’t strictly enforce what’s imported, but you can guide users by explicitly defining a public API within your `__init__.py` file. Python conventions like leading underscores and the `__all__` variable help users understand your intended use.

**When does Python execute the code in `__init__.py`?**
Python executes the code in `__init__.py` the first time you import the package or any of its modules. Python runs this code only once, caching the package for subsequent imports.