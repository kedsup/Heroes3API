import json

import psycopg2
from psycopg2 import sql

from config import dsn
from models.unit import Unit

print(str(dsn))
conn = psycopg2.connect(**dsn)

cursor = conn.cursor()


def init_db():
    """Initializes database"""
    with open('init_db.sql', 'r') as init_file:
        cursor.execute(sql.SQL(init_file.read()))
        conn.commit()


def update_unit(unit: Unit):
    """Updates unit information in database if entry already exists"""
    cursor.execute(
        """UPDATE units
        SET name_ = %s,
            attack = %s,
            defence = %s,
            health = %s,
            min_damage = %s,
            max_damage = %s,
            speed = %s,
            town = %s,
            base_lvl = %s,
            upgrade_lvl = %s,
            growth = %s,
            ai_value = %s,
            cost = %s,
            resources_cost  = %s
        WHERE name_ = %s""", (
            unit.name,
            unit.attack,
            unit.defence,
            unit.health,
            unit.min_damage,
            unit.max_damage,
            unit.speed,
            unit.town,
            unit.base_lvl,
            unit.upgrade_lvl,
            unit.growth,
            unit.ai_value,
            unit.cost,
            json.dumps(unit.resources_cost, indent=4),
            unit.name))
    return True


def add_unit(unit: Unit):
    """Creates unit entry in database"""
    if get_unit_by_name(unit.name):
        update_unit(unit)
        return None
    try:
        cursor.execute(
            """INSERT INTO units (name_, attack, defence, health, min_damage, max_damage,
            speed, town, base_lvl, upgrade_lvl, growth, ai_value, cost, resources_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                unit.name,
                unit.attack,
                unit.defence,
                unit.health,
                unit.min_damage,
                unit.max_damage,
                unit.speed,
                unit.town,
                unit.base_lvl,
                unit.upgrade_lvl,
                unit.growth,
                unit.ai_value,
                unit.cost,
                json.dumps(unit.resources_cost, indent=4)))
        conn.commit()
    except psycopg2.Error as er:
        conn.rollback()
        print(f'Error on add_unit({unit}): {" ".join(er.args)}')
        return False

    return True


def from_db_to_unit_model(unit: tuple) -> Unit:
    """Recieves unit entry from database and converts it into Unit model"""
    return Unit(name=unit[1],
                town=unit[2],
                base_lvl=unit[3],
                upgrade_lvl=unit[4],
                attack=unit[5],
                defence=unit[6],
                min_damage=unit[7],
                max_damage=unit[8],
                health=unit[10],
                speed=unit[11],
                growth=unit[12],
                ai_value=unit[13],
                cost=unit[14],
                resources_cost=json.loads(unit[15]))


def get_unit_by_name(name: str):
    """Recieves unit entry by its name from database and returns it"""
    cursor.execute("""SELECT * FROM units WHERE name_ = %s""", (name,))
    result = cursor.fetchall()
    if len(result) == 0:
        return None
    return from_db_to_unit_model(result[0])
