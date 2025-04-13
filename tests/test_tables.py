from fastapi.testclient import TestClient
import pytest
from app.main import app

client = TestClient(app)

# Тестовые данные для столиков
test_table = {"name": "Table 1", "seats": 4, "location": "Location 1"}


@pytest.fixture
def create_table():
    """
    Фикстура для создания столика перед тестами.
    """
    response = client.post("/tables/", json=test_table)
    assert response.status_code == 200
    return response.json()["id"]


def test_create_table():
    """
    Тест на создание нового столика.
    """
    response = client.post("/tables/", json=test_table)
    assert response.status_code == 200
    assert response.json()["name"] == test_table["name"]
    assert response.json()["seats"] == test_table["seats"]
    assert response.json()["location"] == test_table["location"]


def test_get_table(create_table):
    """
    Тест на получение информации о столике по ID.
    """
    table_id = create_table
    response = client.get(f"/tables/{table_id}")
    assert response.status_code == 200
    assert response.json()["name"] == test_table["name"]


def test_list_tables():
    """
    Тест на получение списка всех столиков.
    """
    response = client.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_table(create_table):
    """
    Тест на обновление информации о столике.
    """
    table_id = create_table
    updated_table = {"name": "New Table", "seats": 6, "location": "Location 2"}
    response = client.put(f"/tables/{table_id}", json=updated_table)
    assert response.status_code == 200
    assert response.json()["name"] == updated_table["name"]
    assert response.json()["seats"] == updated_table["seats"]


def test_delete_table(create_table):
    """
    Тест на удаление столика.
    """
    table_id = create_table
    response = client.delete(f"/tables/{table_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Столик успешно удалён"
