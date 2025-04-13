from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import HTTPException

from app.models.reservation import Reservation
from app.models.table import Table
from app.schemas.reservation import ReservationCreate
from app.utils.logger import logger


def create_reservation(db: Session, reservation: ReservationCreate) -> Reservation:
    """
    Создает новое бронирование.

    :param db: Сессия базы данных.
    :param reservation: Данные для создания бронирования.
    :return: Созданный объект бронирования.
    """
    logger.info(
        "Проверка существования столика с ID: %d",
        reservation.table_id
    )
    table = (db.query(Table)
             .filter(Table.id == reservation.table_id)
             .first()
             )
    if not table:
        logger.error("Столик с ID %d не найден", reservation.table_id)
        raise HTTPException(status_code=404, detail="Столик не найден")

    # Вычисление времени окончания бронирования на стороне Python
    end_time = reservation.reservation_time + timedelta(
        minutes=reservation.duration_minutes
    )

    # Проверка пересечения времени бронирования
    logger.info(
        "Проверка пересечений времени для столика с ID: %d",
        reservation.table_id
    )
    overlapping_reservations = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.reservation_time < end_time,
        Reservation.end_time > reservation.reservation_time
    ).all()

    if overlapping_reservations:
        logger.error(
            "Конфликт времени бронирования для столика с ID: %d",
            reservation.table_id
        )
        raise HTTPException(
            status_code=400,
            detail="Этот столик уже забронирован на выбранное время"
        )

    # Создание нового бронирования
    logger.info(
        "Создание бронирования для клиента: %s",
        reservation.customer_name
    )
    db_reservation = Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes,
        end_time=end_time
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    logger.info("Бронирование успешно создано с ID: %d", db_reservation.id)
    return db_reservation


def list_reservations(db: Session) -> list[Reservation]:
    """
    Возвращает список всех бронирований.

    :param db: Сессия базы данных.
    :return: Список объектов бронирований.
    """
    logger.info("Получение списка всех бронирований")
    reservations = db.query(Reservation).all()
    logger.info("Найдено %d бронирований", len(reservations))
    return reservations


def delete_reservation(db: Session, reservation_id: int) -> None:
    """
    Удаляет бронирование.

    :param db: Сессия базы данных.
    :param reservation_id: ID бронирования.
    """
    logger.info(
        "Проверка существования бронирования с ID: %d",
        reservation_id
    )
    reservation = (db.query(Reservation)
                   .filter(Reservation.id == reservation_id)
                   .first()
                   )
    if not reservation:
        logger.error("Бронирование с ID %d не найдено", reservation_id)
        raise HTTPException(status_code=404, detail="Бронирование не найдено")

    logger.info("Удаление бронирования с ID: %d", reservation_id)
    db.delete(reservation)
    db.commit()
    logger.info("Бронирование с ID %d успешно удалено", reservation_id)
