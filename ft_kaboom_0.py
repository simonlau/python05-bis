#!/usr/bin/env python3

from alchemy.grimoire.light_spellbook import light_spell_record


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    record = light_spell_record("Fantasy", "Earth, wind and fire")
    print(f"Testing record light spell: Spell recorded: {record}")


if __name__ == "__main__":
    main()
