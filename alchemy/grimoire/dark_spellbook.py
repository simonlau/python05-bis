from typing import Literal, TypeAlias

from alchemy.grimoire.dark_validator import validate_ingredients

Ingredient: TypeAlias = Literal["bats", "frogs", "arsenic", "eye-ball"]  # noqa: UP040


def dark_spell_allowed_ingredients() -> list[Ingredient]:
    return ["bats", "frogs", "arsenic", "eye-ball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    result, _ = validate_ingredients(ingredients)
    return f"{spell_name} ({ingredients} - {result})"
