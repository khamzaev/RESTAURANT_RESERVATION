from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.table import TableCreate, TableResponse
from app.services.table_service import (
    create_table, get_table,
    list_tables, update_table, delete_table
)
from app.utils.database import SessionLocal
from app.utils.logger import logger


router = APIRouter(
    prefix="/tables",
    tags=["tables"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=TableResponse)
def create_table_endpoint(table: TableCreate, db: Session = Depends(get_db)):
    logger.info("Создание нового столика: %s", table.name)
    return create_table(db, table)


@router.get("/{table_id}", response_model=TableResponse)
def get_table_endpoint(table_id: int, db: Session = Depends(get_db)):
    logger.info("Получение информации о столике с ID: %d", table_id)
    return get_table(db, table_id)


@router.get("/", response_model=list[TableResponse])
def list_tables_endpoint(db: Session = Depends(get_db)):
    logger.info("Получение списка всех столиков")
    return list_tables(db)


@router.put("/{table_id}", response_model=TableResponse)
def update_table_endpoint(
        table_id: int,
        table: TableCreate,
        db: Session = Depends(get_db)
):
    logger.info("Обновление столика с ID: %d", table_id)
    return update_table(db, table_id, table)


@router.delete("/{table_id}")
def delete_table_endpoint(
        table_id: int,
        db: Session = Depends(get_db)
):
    logger.info("Удаление столика с ID: %d", table_id)
    delete_table(db, table_id)
    return {"detail": "Столик успешно удалён"}
