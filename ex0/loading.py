#!/usr/bin/env python3

import importlib
from importlib.metadata import metadata


def main() -> None:
    print("\nREAGENT STATUS: Loading reagents...\n")

    print("Checking dependencies:")
    module = "pandas"
    try:
        _ = importlib.import_module(module)
        name = metadata(module)["Name"]
        version = metadata(module)["Version"]
        summary = metadata(module)["Summary"]
        print(f"[OK] {name} ({version}) - {summary} ready")
    except ImportError:
        print(f"[KO] {module} not ready")

    module = "numpy"
    try:
        _ = importlib.import_module(module)
        name = metadata(module)["Name"]
        version = metadata(module)["Version"]
        summary = metadata(module)["Summary"]
        print(f"[OK] {name} ({version}) - {summary} ready")
    except ImportError:
        print(f"[KO] {module} not ready")

    msg = """
pip vs Poetry:
  requirements.txt declares what to install; pip resolves it as install time.
  pyproject.toml declaries the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.
"""
    print(msg)


if __name__ == "__main__":
    main()
