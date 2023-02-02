from fastapi.testclient import TestClient

from fastApp import app

client = TestClient(app)


def test_get_unit():
    response = client.get("/unit?name=Zombie")
    assert response.status_code == 200
    assert response.json() == {"ai_value": 128,
                               "attack": 5,
                               "base_lvl": 2,
                               "cost": 125,
                               "defence": 5,
                               "growth": 8,
                               "health": 20,
                               "max_damage": 3,
                               "min_damage": 2,
                               "name": "Zombie",
                               "resources_cost": None,
                               "special": None,
                               "speed": 4,
                               "town": "Necropolis",
                               "upgrade_lvl": 1}


def test_get_unit_inexistent_unit():
    response = client.get("/unit?name=Teletubby")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_get_stack():
    response = client.get("/stack?name=Azure Dragon&size=14")
    assert response.status_code == 200
    assert response.json() == {"name": "Azure Dragon",
                               "attack": 50,
                               "defence": 50,
                               "health": 14000,
                               "min_damage": 980,
                               "max_damage": 1120,
                               "speed": 19,
                               "size": 14}


def test_get_unit_inexistent_unit():
    response = client.get("/stack?name=EGOISTA&size=11")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_get_stack_size_not_int():
    response = client.get("/stack?name=Hobgoblin&size=twelve")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [{"loc": ["query", "size"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer"}]}


def test_get_stack_bad_size_num():
    response = client.get("/stack?name=Fangarm&size=0")
    assert response.status_code == 400
    assert response.json() == {"detail": "Size must be greater than zero"}
