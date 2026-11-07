#!/usr/bin/env python3


def main() -> None:
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    try:
        from alchemy.grimoire.dark_spellbook import dark_spell_record

        record = dark_spell_record("Fantasy", "Earth, wind and fire")
        print(f"Testing record dark spell: Spell recorded: {record}")
    except ImportError as error:
        print(error)


if __name__ == "__main__":
    main()
