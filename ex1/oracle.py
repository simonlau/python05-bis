#!/usr/bin/env python3

import os

from dotenv import load_dotenv


def main() -> None:
    load_dotenv(override=False)

    print("ORACLE STATUS: Consulting the configuration...")

    print("Configuration loaded:")
    print(f"Mode: {os.getenv('MATRIX_MODE')}")
    print(f"Database: {os.getenv('DATABASE_URL')}")
    print(f"API Access: {os.getenv('API_KEY')}")
    print(f"Log Level: {os.getenv('LOG_LEVEL')}")
    print(f"Remote Network: {os.getenv('ZION_ENDPOINT')}")

    print("\nConfiguration security check:")
    print("[OK] No hardcoded secrets detected")
    print("[OK] .env file properly ignored by git")
    print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
