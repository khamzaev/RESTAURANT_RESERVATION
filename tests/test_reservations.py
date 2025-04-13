import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.main import app


client = TestClient(app)

# Тестовые данные для столиков и бронирования
test_table = {"name": "Table 1", "seats": 4, "location": "Location 1"}
test_reservation = {
    "customer_name": "Ivan Ivanov",
    "table_id": 1,
    "reservation_time": (datetime.now() + timedelta(hours=1)).isoformat(),
    "duration_minutes": 60,
}

@pytest.fixture
def create_table():
    """
    Фикстура для создания столика перед тестами.
    """
    response = client.post("/tables/", json=test_table)
    assert response.status_code == 200
    return response.json()["id"]


def test_create_reservation(client, create_table):
    """
    Тест на создание нового бронирования.
    """
    test_reservation["table_id"] = create_table
    response = client.post("/reservations/", json=test_reservation)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == test_reservation["customer_name"]
    assert data["table_id"] == test_reservation["table_id"]


def test_list_reservations(create_table):
    """
    Тест на получение списка всех бронирований.
    """
    test_reservation["table_id"] = create_table
    client.post("/reservations/", json=test_reservation)
    response = client.get("/reservations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_delete_reservation(create_table):
    """
    Тест на удаление бронирования.
    """
    # Создаем бронирование
    test_reservation["table_id"] = create_table
    response = client.post("/reservations/", json=test_reservation)
    reservation_id = response.json()["id"]

    # Удаляем бронирование
    response = client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Бронирование успешно удалено"
