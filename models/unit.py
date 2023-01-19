from typing import Union
import re
from pydantic import BaseModel, validator


class Unit(BaseModel):
    ai_value: int
    attack: int
    base_lvl: int
    cost: int
    defense: int
    growth: int
    hp: int
    max_dmg: int
    min_dmg: int
    name: str
    resources_cost: Union[dict | None]
    special: Union[str | None]
    speed: int
    town: str
    upgrade_lvl: int

    @validator('ai_value', 'attack', 'base_lvl', 'cost',
               'defense', 'growth', 'hp', 'max_dmg', 'min_dmg', 'speed')
    def pos_int_validator(cls, v):
        if v < 1:
            raise ValueError(f'{v} must be equal to or greater than 1')
        return v

    @validator('min_dmg')
    def min_dmg_smaller_validator(cls, v, values):
        if 'max_dmg' in values and v > values['max_dmg']:
            raise ValueError(f'min_dmg {v} must be less than or equal to max_dmg')
        return v

    @validator('name', 'town')
    def name_town_validator(cls, v):
        if re.search(r"(.*\W)", v) or re.search(r"(.*[0-9])", v):
            raise ValueError('String must not contain Any Non-alphanumeric characters and/or Any Numeric characters')
        return v
