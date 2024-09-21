from pydantic import BaseModel, EmailStr, constr
from typing import Optional

# Модели Pydantic для пользователя

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
    email: EmailStr  # Используем EmailStr для валидации email

class CreateUser(BaseModel):
    """
    Модель для создания нового пользователя.

    Атрибуты:
        name (str): Имя пользователя.
        email (EmailStr): Электронная почта пользователя, валидируемая с помощью EmailStr.
        password (constr): Пароль пользователя, минимальная длина 5 символов.
    """
    name: str
    email: EmailStr  # Используем EmailStr для валидации email
    password: constr(min_length=5)  # Устанавливаем минимальную длину пароля

# Модели Pydantic для задач

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
    description: Optional[str] = None  # Поле description может быть None
    status: str

class UpdateTask(BaseModel):
    """
    Модель для обновления информации о задаче.

    Атрибуты:
        status (str): Статус задачи для обновления.
    """
    status: str  # Позволяет обновить статус задачи

class CreateTask(BaseModel):
    """
    Модель для создания новой задачи.

    Атрибуты:
        title (str): Название задачи.
        description (Optional[str]): Описание задачи, может быть None.
        status (str): Статус задачи.
    """
    title: str  # Название задачи
    description: Optional[str] = None  # Поле description может быть None
    status: str  # Строка со статусом задачи