from typing import Literal, TypeAlias

Ingredient: TypeAlias = Literal["earth", "air", "fire", "water"]  # noqa: UP040


def light_spell_allowed_ingredients() -> list[Ingredient]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire.light_validator import validate_ingredients  # noqa: PLC0415

    result, _ = validate_ingredients(ingredients)
    return f"{spell_name} ({ingredients} - {result})"
