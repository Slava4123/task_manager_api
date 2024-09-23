"""Модели Pydantic для пользователя и задач"""

from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class ReadUser(BaseModel):
    """
    Модель для чтения информации о пользователе.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя.
        name (str): Имя пользователя.
        email (EmailStr): Электронная почта пользователя, валидируемая с помощью EmailStr.
    """
    id: int
    name: str
    email: EmailStr


class CreateUser(BaseModel):
    """
    Модель для создания нового пользователя.

    Атрибуты:
        name (str): Имя пользователя.
        email (EmailStr): Электронная почта пользователя, валидируемая с помощью EmailStr.
        password (constr): Пароль пользователя, минимальная длина 5 символов.
    """
    name: str
    email: EmailStr
    password: constr(min_length=5)




class ReadTask(BaseModel):
    """
    Модель для чтения информации о задаче.

    Атрибуты:
        id (int): Уникальный идентификатор задачи.
        title (str): Заголовок задачи.
        description (Optional[str]): Описание задачи, может быть None.
        status (str): Статус задачи.
    """
    id: int
    title: str
    description: Optional[str] = None
    status: str


class UpdateTask(BaseModel):
    """
    Модель для обновления информации о задаче.

    Атрибуты:
        status (str): Статус задачи для обновления.
    """
    status: str


class CreateTask(BaseModel):
    """
    Модель для создания новой задачи.

    Атрибуты:
        title (str): Название задачи.
        description (Optional[str]): Описание задачи, может быть None.
        status (str): Статус задачи.
    """
    title: str
    description: Optional[str] = None
    status: str