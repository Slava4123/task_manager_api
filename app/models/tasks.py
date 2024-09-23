from app.database.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Task(Base):
    """
    Модель задачи.

    Атрибуты:
        id (int): Уникальный идентификатор задачи.
        title (str): Название задачи.
        description (str): Описание задачи (может быть пустым).
        status (str): Статус задачи.
        user_id (int): Идентификатор пользователя, которому принадлежит задача.

    Связи:
        user (User): Отношение, связывающее задачу с пользователем.
    """
    __tablename__ = 'tasks'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # Связь с пользователем
    user = relationship('User', back_populates='tasks')


