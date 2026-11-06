#!/usr/bin/env python3

import os.path
import site
import sys


def main() -> None:
    is_in_venv = sys.prefix != sys.base_prefix
    status = "The laboratory is sealed" if is_in_venv else "You are working in the open"
    print(f"LABORATORY STATUS {status}:")

    print(f"Current Python: {sys.base_prefix}")
    if not is_in_venv:
        print("Virtual Environment: None detected")
    else:
        venv_dir = os.path.basename(os.path.normpath(sys.prefix))
        print(f"Virtual Environment: {venv_dir}")
        print(f"Environment Path: {sys.prefix}")

    if is_in_venv:
        msg = f"""
SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting the global system.

Reagent installation path:
{site.getsitepackages()}
"""
    else:
        msg = """
WARNING: You are in the global environment!
Every reagent you install here leaks into the whole system

To seal the laboratory, run:
python3 -m venv lab_env  # or uv venv
source lab_env/bin/activate # On Unix
lab_env\\Scripts\\activate # On Windows

Then run this program again
        """
    print(msg)


if __name__ == "__main__":
    main()
