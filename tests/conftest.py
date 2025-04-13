import os
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.utils.database import Base



# URL для тестовой базы данных
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Переменная окружения DATABASE_URL не задана!")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@pytest.fixture
def client():
    """
    Pytest фикстура для создания клиента TestClient.
    """
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    """
    Фикстура для настройки тестовой базы данных перед выполнением тестов.
    """
    # Удаляем и создаем заново все таблицы для тестов
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Очистка после выполнения всех тестов (опционально)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """
    Фикстура для создания сессии базы данных.
    """
    session = Session()
    yield session
    session.close()
