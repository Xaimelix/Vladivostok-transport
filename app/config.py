"""
Конфигурация приложения
"""
import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent

# Параметры БД
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "sqlite:///./Info.sqlite3"
)

# Параметры приложения
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
