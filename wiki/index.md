# Knowledge Base Index

## python-programming

**Python 3.10+ package architecture, environments, and configuration course**

| Article | Summary | Updated |
|---------|---------|---------|
| [The Codex: Packages, Environments and the Alchemist's Toolchain](python-programming/the-codex-packages-environments-and-alchemy-toolchain.md) | Comprehensive Python 3.10+ course covering virtual environments, dependency management, package structure, circular dependencies, and configuration systems with alchemical metaphors. | 2026-11-02 |
| [Python Package Structure Basics](python-programming/python-package-basics.md) | Foundational Python package architecture including `__init__.py` as package marker, namespace packages vs regular packages, `__init__.py` execution timing and caching, `__all__` variable, underscore conventions for non-public names, explicit public API, and top-level package metadata. | 2026-11-07 |
| [Python Dotenv Usage](python-programming/python-dotenv-usage.md) | Environment variable configuration using python-dotenv 1.2.4, .env files, CLI interface, file format, variable expansion precedence, IPython support, security best practices, and testing patterns. | 2026-11-06 |
| [Python Imports Guide](python-programming/python-imports-guide.md) | Python import mechanisms: standard imports, absolute vs relative imports, namespace packages, resource imports (importlib.resources), dynamic imports (importlib), import system internals, cyclical imports, and import profiling. | 2026-11-06 |
| [Virtual Environment Management](python-programming/virtual-environment-management.md) | Creating, activating, and managing Python virtual environments: folder structure, pyvenv.cfg, prefix-finding, isolation mechanics, venv alternatives (virtualenv, conda), dependency pinning, IDE integration, and detection methods (sys.prefix, VIRTUAL_ENV). | 2026-11-06 |
| [Python Dependency Management](python-programming/python-dependency-management.md) | Comparing pip (requirements.txt), Poetry (pyproject.toml + poetry.lock), and uv (pyproject.toml + uv.lock) for dependency management with reproducibility best practices. uv is 10–100x faster than pip and replaces multiple tools. | 2026-11-06 |
| [Python pip: Standard Package Manager](python-programming/python-pip.md) | Python’s built-in package manager: finding pip, running as module, virtual environments, installing from PyPI/custom indexes/git repos, requirements files, uninstalling, and alternatives. | 2026-11-06 |
| [Python uv: All-in-One Package and Project Manager](python-programming/python-uv.md) | Rust-based all-in-one Python package and project manager: fast dependency installation, automatic virtual environments, Python version management, project initialization, dependency locking, and package publishing. | 2026-11-06 |
| [Circular Dependency Management](python-programming/circular-dependency-management.md) | Understanding, detecting, and resolving circular import dependencies: `sys.modules` cache behavior, `ImportError` vs `AttributeError`, shop package example, `TYPE_CHECKING` guard, workarounds (defer imports, move to bottom, change import form), and Python 3.15 PEP 810 lazy import. | 2026-11-07 |