"""
Модуль для управления соединением с базой данных.

Этот модуль содержит классы и функции, необходимые для создания
и управления сессиями базы данных с использованием SQLAlchemy.
Обеспечивает создание и настройку асинхронного подключения к базе данных.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .db import SessionLocal
import loguru

async def get_db() -> AsyncSession:
    """
    Асинхронный генератор для получения сессии базы данных.

    Используется для управления сессиями базы данных в приложении.
    Генерирует сессию, которая автоматически закрывается в конце блока.

    Возвращает:
        AsyncSession: Асинхронная сессия базы данных.

    Исключения:
        SQLAlchemyError: Возникает при ошибках SQLAlchemy.
    """
    async with SessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            loguru.logger.error(f"Произошла ошибка: {e}")
            await session.rollback()
            raise