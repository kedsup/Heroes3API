from typing import Union
import re

from pydantic import BaseModel, validator


class Unit(BaseModel):
    ai_value: int
    attack: int
    base_lvl: int
    cost: int
    defence: int
    growth: int
    health: int
    max_damage: int
    min_damage: int
    name: str
    resources_cost: Union[dict | None]
    special: Union[str | None]
    speed: int
    town: str
    upgrade_lvl: int

    @validator('ai_value', 'attack', 'base_lvl', 'cost',
               'defence', 'growth', 'health', 'max_damage', 'min_damage', 'speed')
    def pos_int_validator(cls, v):
        if v < 1:
            raise ValueError(f'{v} must be equal to or greater than 1')
        return v

    @validator('min_damage')
    def min_dmg_smaller_validator(cls, v, values):
        if 'max_damage' in values and v > values['max_damage']:
            raise ValueError(f'min_damage {v} must be less than or equal to max_damage')
        return v

    @validator('name', 'town')
    def name_town_validator(cls, v):
        if re.search(r"[^A-Za-z ]+", v):
            raise ValueError(
                'String must not contain Any Non-alphanumeric characters, except spaces and/or Any Numeric characters')
        return v
