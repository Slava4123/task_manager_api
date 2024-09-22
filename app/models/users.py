from app.database.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """
    Модель пользователя.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        name (str): Имя пользователя.
        email (str): Электронная почта пользователя, должна быть уникальной.
        password (str): Пароль пользователя (возможно, должен храниться в хэшированном виде).

    Связи:
        tasks (list[Task]): Список задач, связанных с пользователем.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # Limited to 50 characters
    email = Column(String(120), nullable=False, unique=True)  # Limited to 120 characters
    password = Column(String(128), nullable=False)  # Limited to 128 characters

    # Связь с задачами
    tasks = relationship('Task', back_populates='user')
