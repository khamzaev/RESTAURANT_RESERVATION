from pydantic import BaseModel, Field, validator
from datetime import datetime

class ReservationBase(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    table_id: int
    reservation_time: datetime
    duration_minutes: int

    @validator("reservation_time")
    def validate_reservation_time(cls, value):
        if value < datetime.now():
            raise ValueError("Время бронирования не может быть в прошлом")
        return value

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    id: int

    class Config:
        orm_mode = True
