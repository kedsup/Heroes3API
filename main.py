from pprint import pprint
import json

from db import add_unit, get_unit_by_name, init_db
from parsing import get_unit_stats
from models.unit import Unit


def main():
    """Gets unit stats"""
    init_db()

    name_unit = get_unit_stats()

    for _, unit in name_unit.items():
        unit_model = Unit(**unit)
        add_unit(unit_model)

    print(get_unit_by_name('Azure Dragon'))
    json_azure_dragon = json.dumps(name_unit['azure_dragon'], indent=4)
    unit = Unit.parse_raw(json_azure_dragon)
    print(unit.json())


if __name__ == '__main__':
    main()
