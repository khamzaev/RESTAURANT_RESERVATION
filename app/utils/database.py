import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test_user:test_password@localhost:5432/test_db")

# Создаем подключение к PostgreSQL
engine = create_engine(DATABASE_URL)

# Определяем базовый класс для моделей
Base = declarative_base()

# Создаем сессию для взаимодействия с базой данных
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
