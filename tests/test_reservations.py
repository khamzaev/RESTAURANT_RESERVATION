from fastapi.testclient import TestClient
from datetime import datetime, timedelta

from app.main import app

client = TestClient(app)

# Тестовые данные для бронирования
test_table = {"name": "Столик 1", "seats": 4, "location": "Зал 1"}
test_reservation = {
    "customer_name": "Иван Иванов",
    "table_id": 1,
    "reservation_time": (datetime.now() + timedelta(hours=1)).isoformat(),
    "duration_minutes": 60
}

def test_create_reservation():
    """
    Тест на создание нового бронирования.
    """
    # Создаем столик для бронирования
    response = client.post("/tables/", json=test_table)
    table_id = response.json()["id"]

    test_reservation["table_id"] = table_id
    response = client.post("/reservations/", json=test_reservation)
    assert response.status_code == 200
    assert response.json()["customer_name"] == test_reservation["customer_name"]
    assert response.json()["table_id"] == test_reservation["table_id"]

def test_list_reservations():
    """
    Тест на получение списка всех бронирований.
    """
    response = client.get("/reservations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_reservation():
    """
    Тест на удаление бронирования.
    """
    # Создаем бронирование
    response = client.post("/tables/", json=test_table)
    table_id = response.json()["id"]

    test_reservation["table_id"] = table_id
    response = client.post("/reservations/", json=test_reservation)
    reservation_id = response.json()["id"]

    # Удаляем бронирование
    response = client.delete(f"/reservations/{reservation_id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Бронирование успешно удалено"
