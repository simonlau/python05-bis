#!/usr/bin/env python3

import importlib
from importlib.metadata import metadata


def main() -> None:
    print("REAGENT STATUS: Loading reagents...")

    print("Checking dependencies:")
    try:
        _ = importlib.import_module("pandas")
        name = metadata("pandas")["Name"]
        version = metadata("pandas")["Version"]
        summary = metadata("pandas")["Summary"]
        print(f"[OK] {name} ({version}) - {summary} ready")
    except ImportError:
        print("[KO] pandas not ready")

    try:
        _ = importlib.import_module("numpy")
        name = metadata("numpy")["Name"]
        version = metadata("numpy")["Version"]
        summary = metadata("numpy")["Summary"]
        print(f"[OK] {name} ({version}) - {summary} ready")
    except ImportError:
        print("[KO] numpy not ready")

    msg = """
pip vs Poetry:
  requirements.txt declares what to install; pip resolves it as install time.
  pyproject.toml declaries the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical
"""
    print(msg)


if __name__ == "__main__":
    main()
