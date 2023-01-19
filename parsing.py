from typing import Dict, Optional, Tuple
import re

import requests
from bs4 import BeautifulSoup, ResultSet
from exceptions import IncorrectHttpResponseException


def get_html_page(url: str) -> BeautifulSoup:
    """Gets html page using BeautifulSoup"""
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise IncorrectHttpResponseException
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_trs_from_html_doc(doc) -> ResultSet:
    """Gets table rows"""
    table_rows = doc.find(name='table', attrs={'class': "sortable"}).tbody.find_all('tr')
    return table_rows[1:]


def _get_unit_key(tds) -> str:
    """Gets the key, which is the name of the unit"""
    key_td = tds[0]
    key_value = key_td.find_all('a')[1].text.strip()
    key = key_value.replace(' ', '_').lower()
    return key


def _get_basic_stats(tds) -> dict:
    """Gets basic stats of the unit"""
    name_td = tds[0]
    attack_td = tds[3]
    defence_td = tds[4]
    min_damage_td = tds[5]
    max_damage_td = tds[6]
    health_td = tds[7]
    speed_td = tds[8]

    name = name_td.find_all('a')[1].text.strip()
    attack = int(attack_td.find('span', {'title': 'Attack'}).text.strip())
    defence = int(defence_td.find('span', {'title': 'Defense'}).text.strip())
    health = int(health_td.find('span', {'title': 'Health'}).text.strip())
    min_damage = int(min_damage_td.find('span', {'title': 'Minimum Damage'}).text.strip())
    max_damage = int(max_damage_td.find('span', {'title': 'Maximum Damage'}).text.strip())
    speed = int(speed_td.find('span', {'title': 'Speed'}).text.strip())

    return {
        'name': name,
        'attack': attack,
        'defense': defence,
        'hp': health,
        'min_dmg': min_damage,
        'max_dmg': max_damage,
        'speed': speed
    }


def _get_additional_stats(tds):
    """Gets additional stats of the unit"""
    town_td = tds[1]
    lvl_td = tds[2]
    growth_td = tds[9]
    ai_value_td = tds[10]
    cost_td = tds[11]
    resources_cost_td = tds[12]
    special_td = tds[13]

    town = town_td.find('span').get('title')
    lvl_text = lvl_td.find('span', {'title': 'Level'}).text.strip()
    base_lvl, upgrade_lvl = _convert_to_int_lvl(lvl_text)
    cost = int(cost_td.text.strip())
    growth = int(growth_td.find('span', {'title': 'Growth'}).text.strip())
    ai_value = int(ai_value_td.find('span', {'title': 'AI_Value'}).text.strip())
    resources_cost_dict = _get_resources_cost(resources_cost_td)
    special = special_td.text.replace('\n', ' ').strip()
    return {
        'town': town,
        'base_lvl': base_lvl,
        'upgrade_lvl': upgrade_lvl,
        'growth': growth,
        'ai_value': ai_value,
        'cost': cost,
        'resources_cost': resources_cost_dict,
        'special': special
    }


def get_unit_stats() -> Optional[Dict]:
    """Gets unit stats"""
    name_stat = {}
    try:
        soup = get_html_page('https://heroes.thelazy.net/index.php/List_of_creatures_(HotA)')
    except IncorrectHttpResponseException:
        print('Couldn\'t get html')
        return None
    table_rows = get_trs_from_html_doc(soup)

    for row in table_rows:
        tds = row.find_all('td')
        key = _get_unit_key(tds)

        name_stat[key] = _get_basic_stats(tds)
        name_stat[key].update(_get_additional_stats(tds))

    return name_stat


def _convert_to_int_lvl(lvl_text: Optional[str]) -> Tuple[int, int]:
    """Converts level text into base_lvl: int and upgrade_lvl:int"""
    if not lvl_text:
        return 0, 0
    base_lvl = int(lvl_text.replace('+', ''))
    upgrade_lvl = lvl_text.count('+')
    return base_lvl, upgrade_lvl


def _get_resources_cost(resources_cost_td) -> Optional[Tuple[str, int]]:
    """Converts resources text into resource:str and resources_cost:int"""
    if not resources_cost_td:
        return None
    resource, resources_cost = None, None
    res = re.search(r'\d+', resources_cost_td.text)

    if res:
        resources_cost = res.group()
        resource = resources_cost_td.find('a').get('title')

    resources_cost_dict = {resource: resources_cost} if resource else None

    return resources_cost_dict
