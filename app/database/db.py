"""
Этот файл настраивает подключение к базе данных и определяет базовую модель для SQLAlchemy.

Он загружает переменные среды из файла `.env`, создает асинхронный движок базы данных
и определяет создателя сессий для создания асинхронных сессий базы данных.

Функция `check_connection` проверяет подключение к базе данных, выполняя простой запрос.
Класс `Base` - это декларативный базовый класс для моделей SQLAlchemy.
"""

import os
import loguru

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def check_connection():
    """
    Проверяет подключение к базе данных.

    Устанавливает соединение с базой данных и выполняет
    запрос для проверки работоспособности. Выводит сообщение
    о статусе подключения.

    Исключения:
        Exception: Возникает при ошибках подключения к базе данных.
    """
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
            loguru.logger.info("Подключение к базе данных успешно установлено.")
    except Exception as e:
        loguru.logger.error(f"Ошибка подключения к базе данных: {e}")

class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.

    Используется в качестве основы для всех моделей в приложении.
    Позволяет использовать декларативный стиль определения моделей.
    """
    pass
