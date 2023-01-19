from pprint import pprint
from parsing import get_unit_stats
from models.unit import Unit


def main():
    """Gets unit stats"""
    name_unit = get_unit_stats()
    pprint(name_unit)
    ayssid = name_unit['ayssid']
    pprint(ayssid)
    unit = Unit(**ayssid) #ZAEBIS
    pprint(unit)
    print({**ayssid})


if __name__ == '__main__':
    main()
