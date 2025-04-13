import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()


print(sys.executable)

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Отладочный вывод
print(f"DATABASE_URL: {DATABASE_URL}")

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
