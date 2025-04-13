from fastapi import FastAPI

from app.routers import tables, reservations


app = FastAPI(
    title="API для бронирования столиков",
    description="API для управления столиками и бронированиями в ресторане",
    version="1.0.0",
)

# Подключение роутеров
app.include_router(tables.router)
app.include_router(reservations.router)

@app.get("/")
def read_root():
    """
    Корневой маршрут для проверки работы API.
    """
    return {"message": "Добро пожаловать в API бронирования столиков"}
