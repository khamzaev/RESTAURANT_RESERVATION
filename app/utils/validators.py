from datetime import datetime

def validate_reservation_time(reservation_time: datetime) -> None:
    """
    Проверяет, чтобы время бронирования было в будущем.

    :param reservation_time: Время бронирования.
    """
    if reservation_time < datetime.now():
        raise ValueError("Время бронирования не может быть в прошлом")
