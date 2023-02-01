from fastapi import HTTPException

import db


def get_unit(name: str):
    """Returns unit model from db"""
    response = db.get_unit_by_name(name)
    if not response:
        raise HTTPException(status_code=404, detail="Item not found")
    return response


def calculate_stack(name: str, size: int):
    """Returns dict with stack of unit info"""
    response = db.get_unit_by_name(name)
    if not response:
        raise HTTPException(status_code=404, detail="Item not found")

    stack = {
        'name': name,
        'attack': response.attack,
        'defence': response.defence,
        'health': response.health * size,
        'min_damage': response.min_damage * size,
        'max_damage': response.max_damage * size,
        'speed': response.speed,
        'size': size
    }

    return stack
