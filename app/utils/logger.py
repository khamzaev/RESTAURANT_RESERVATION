import logging


# Настройка форматирования логов
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Создаем базовый логгер
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format=LOG_FORMAT,
)

# Получаем логгер приложения
logger = logging.getLogger("restaurant_reservation")