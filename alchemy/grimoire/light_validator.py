from typing import Literal, TypeAlias

from alchemy.grimoire.light_spellbook import light_spell_allowed_ingredients

Result: TypeAlias = Literal["VALID", "INVALID"]
ValidateResult: TypeAlias = tuple[Result, str]


def validate_ingredients(ingredients: str) -> ValidateResult:
    valid_list = light_spell_allowed_ingredients()
    input_list = ingredients.split()
    result = any(True for x in input_list if x in valid_list)
    if result:
        return "VALID", ingredients
    return "INVALID", ingredients
