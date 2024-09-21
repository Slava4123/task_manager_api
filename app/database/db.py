import os

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# URL подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Создание асинхронного движка базы данных
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание фабрики сессий
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
            print("Подключение к базе данных успешно установлено.")
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")

class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.

    Используется в качестве основы для всех моделей в приложении.
    Позволяет использовать декларативный стиль определения моделей.
    """
    pass
