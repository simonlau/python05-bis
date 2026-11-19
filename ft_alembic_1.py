#!/usr/bin/env python3

import alchemy


def main() -> None:
    print("=== Alembic 1 ===")
    print(f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth:", end="")
    try:
        # pyrefly: ignore[missing-attribute]
        print(f"{alchemy.create_earth()}")
    except ImportError as error:
        print(f"{error}")


if __name__ == "__main__":
    main()
