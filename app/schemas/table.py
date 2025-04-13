from pydantic import BaseModel


class TableBase(BaseModel):
    name: str
    seats: int
    location: str

class TableCreate(TableBase):
    pass

class TableResponse(TableBase):
    id: int

    class Config:
        orm_mode = True
