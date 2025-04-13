from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session



from app.schemas.reservation import ReservationCreate, ReservationResponse
from app.services.reservation_service import create_reservation, list_reservations, delete_reservation
from app.utils.database import SessionLocal
from app.utils.logger import logger

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ReservationResponse)
def create_reservation_endpoint(reservation: ReservationCreate, db: Session = Depends(get_db)):
    logger.info("Создание нового бронирования для клиента: %s", reservation.customer_name)
    return create_reservation(db, reservation)

@router.get("/", response_model=list[ReservationResponse])
def list_reservations_endpoint(db: Session = Depends(get_db)):
    logger.info("Получение списка всех броней")
    return list_reservations(db)

@router.delete("/{reservation_id}")
def delete_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    logger.info("Удаление бронирования с ID: %d", reservation_id)
    delete_reservation(db, reservation_id)
    return {"detail": "Бронирование успешно удалено"}
