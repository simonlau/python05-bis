from typing import Literal, TypeAlias

from alchemy.grimoire.dark_spellbook import dark_spell_allowed_ingredients

Result: TypeAlias = Literal["VALID", "INVALID"]
ValidateResult: TypeAlias = tuple[Result, str]


def validate_ingredients(ingredients: str) -> ValidateResult:
    valid_list = dark_spell_allowed_ingredients()
    input_list = ingredients.split()
    result = any(True for x in input_list if x in valid_list)
    if result:
        return "VALID", ingredients
    return "INVALID", ingredients
