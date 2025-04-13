# API для бронирования столиков в ресторане

## Описание
Проект представляет собой REST API для управления столиками и бронированиями в ресторане. Реализованы основные функции:
- CRUD-операции для столиков.
- Создание и удаление бронирований.
- Проверка доступности столиков.

---

## Технологии
- Python 3.11
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic для миграций
- Docker и Docker Compose
- Pytest для тестирования

---

## Установка и запуск

### 1. Клонирование репозитория
Клонируйте проект на вашу локальную машину:
```bash
git clone https://github.com/khamzaev/restaurant_reservation.git
cd restaurant_reservation
```

---

---

### 3. Запуск через Docker
Убедитесь, что у вас установлен Docker и Docker Compose. Затем выполните команду:
```bash
docker-compose up --build
```

### 4. Автоматические миграции
При каждом старте контейнера приложение автоматически выполняет миграции с помощью Alembic. Вы также можете вручную выполнить миграции:
```bash
docker-compose exec app alembic upgrade head
```

---

## Тестирование
Для запуска тестов выполните команду:
```bash
pytest tests/
```

---

## Примеры запросов

### 1. Создать новый столик
**POST** `/tables/`
```json
{
  "name": "Столик 1",
  "seats": 4,
  "location": "Зал 1"
}
```

### 2. Получить список столиков
**GET** `/tables/`

### 3. Создать бронирование
**POST** `/reservations/`
```json
{
  "customer_name": "Иван Иванов",
  "table_id": 1,
  "reservation_time": "2025-04-13T15:00:00",
  "duration_minutes": 60
}
```

### 4. Проверить доступные столики
**GET** `/reservations/availability?start_time=2025-04-13T15:00:00&end_time=2025-04-13T17:00:00`

---

## Структура проекта
```
restaurant-reservation/
├── alembic/                 # Директория для миграций Alembic
│   ├── versions/            # Файлы версий миграций
│   └── env.py               # Конфигурация Alembic
├── app/                     # Основное приложение
│   ├── __init__.py          # Инициализация приложения
│   ├── main.py              # Точка входа в приложение (FastAPI)
│   ├── database.py          # Настройка подключения к базе данных
│   ├── models/              # SQLAlchemy/SQLModel модели
│   │   ├── __init__.py
│   │   ├── table.py         # Модель "Table"
│   │   └── reservation.py   # Модель "Reservation"
│   ├── routers/             # Роутеры для API
│   │   ├── __init__.py
│   │   ├── tables.py        # Роуты для работы со столиками
│   │   └── reservations.py  # Роуты для работы с бронями
│   ├── schemas/             # Pydantic-схемы для валидации
│   │   ├── __init__.py
│   │   ├── table.py         # Схемы для "Table"
│   │   └── reservation.py   # Схемы для "Reservation"
│   ├── services/            # Бизнес-логика приложения
│   │   ├── __init__.py
│   │   ├── table_service.py # Логика для работы со столиками
│   │   └── reservation_service.py # Логика для работы с бронями
│   └── utils/               # Утилиты (например, для обработки ошибок)
│       ├── __init__.py
│       └── validators.py    # Валидации (например, проверка пересечений времени)
├── tests/                   # Тесты
│   ├── __init__.py
│   ├── test_tables.py       # Тесты для столиков
│   └── test_reservations.py # Тесты для броней
├── .env                     # Настройки окружения (например, переменные для подключения к БД)
├── .gitignore               # Исключения для git
├── Dockerfile               # Dockerfile для контейнеризации приложения
├── docker-compose.yml       # Конфигурация docker-compose
├── requirements.txt         # Зависимости Python
└── README.md                # Инструкция для проекта
```

---

## Автор
[Ваше имя или команда]