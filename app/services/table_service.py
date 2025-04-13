from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.table import Table
from app.schemas.table import TableCreate
from app.utils.logger import logger


def create_table(db: Session, table: TableCreate) -> Table:
    """
    Создает новый столик в базе данных.

    :param db: Сессия базы данных.
    :param table: Данные для создания столика.
    :return: Созданный объект столика.
    """
    logger.info("Создание нового столика: %s", table.name)
    db_table = Table(
        name=table.name,
        seats=table.seats,
        location=table.location
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    logger.info("Столик успешно создан с ID: %d", db_table.id)
    return db_table


def get_table(db: Session, table_id: int) -> Table:
    """
    Возвращает столик по его ID.

    :param db: Сессия базы данных.
    :param table_id: ID столика.
    :return: Объект столика.
    """
    logger.info("Получение информации о столике с ID: %d", table_id)
    table = db.query(Table).filter(Table.id == table_id).first()
    if not table:
        logger.error("Столик с ID %d не найден", table_id)
        raise HTTPException(status_code=404, detail="Столик не найден")
    logger.info("Информация о столике с ID %d успешно получена", table_id)
    return table


def list_tables(db: Session) -> list[Table]:
    """
    Возвращает список всех столиков.

    :param db: Сессия базы данных.
    :return: Список объектов столиков.
    """
    logger.info("Получение списка всех столиков")
    tables = db.query(Table).all()
    logger.info("Найдено %d столиков", len(tables))
    return tables


def update_table(db: Session, table_id: int, table: TableCreate) -> Table:
    """
    Обновляет информацию о столике.

    :param db: Сессия базы данных.
    :param table_id: ID столика.
    :param table: Новые данные для столика.
    :return: Обновленный объект столика.
    """
    logger.info("Обновление столика с ID: %d", table_id)
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if not db_table:
        logger.error("Столик с ID %d не найден", table_id)
        raise HTTPException(status_code=404, detail="Столик не найден")
    db_table.name = table.name
    db_table.seats = table.seats
    db_table.location = table.location
    db.commit()
    db.refresh(db_table)
    logger.info("Столик с ID %d успешно обновлен", table_id)
    return db_table


def delete_table(db: Session, table_id: int) -> None:
    """
    Удаляет столик из базы данных.

    :param db: Сессия базы данных.
    :param table_id: ID столика.
    """
    logger.info("Удаление столика с ID: %d", table_id)
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if not db_table:
        logger.error("Столик с ID %d не найден", table_id)
        raise HTTPException(status_code=404, detail="Столик не найден")
    db.delete(db_table)
    db.commit()
    logger.info("Столик с ID %d успешно удален", table_id)
