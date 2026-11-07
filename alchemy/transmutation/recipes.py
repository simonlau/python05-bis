# ruff: ignore [INP001]
from alchemy import create_air
from alchemy.potions import strength_potion
from elements import create_fire


def lead_to_gold() -> str:
    air = create_air()
    fire = create_fire()
    parts = f"brew '{air}' and '{strength_potion}' mixed with '{fire}'"
    return f"Recipe transmuting Lead to Gold: {parts}"
