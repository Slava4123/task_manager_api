from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_session import get_db
from typing import Annotated
from app.models import User
from sqlalchemy import select
from app.schemas import CreateUser, ReadUser
from passlib.context import CryptContext

router = APIRouter(prefix='/users', tags=['Users'])
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@router.get('', response_model=list[ReadUser])
async def all_users(db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Получение списка всех пользователей.

    Аргументы:
        db (AsyncSession): Сессия базы данных.

    Возвращает:
        list[ReadUser]: Список пользователей.

    Исключения:
        HTTPException: Если пользователи не найдены или возникает ошибка сервера.
    """
    try:
        result = await db.scalars(select(User))
        users = result.all()

        if not users:
            raise HTTPException(status_code=404, detail="Пользователи не найдены")

        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/{user_id}', response_model=ReadUser)
async def get_user(db: Annotated[AsyncSession, Depends(get_db)], user_id: int):
    """
    Получение пользователя по его идентификатору.

    Аргументы:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя.

    Возвращает:
        ReadUser: Данные пользователя.

    Исключения:
        HTTPException: Если пользователь не найден.
    """
    user = await db.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    return user


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CreateUser)
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: CreateUser):
    """
    Создание нового пользователя.

    Аргументы:
        db (AsyncSession): Сессия базы данных.
        create_user (CreateUser): Данные для создания нового пользователя.

    Возвращает:
        CreateUser: Созданный пользователь.

    Исключения:
        HTTPException: Если пользователь с таким адресом электронной почты уже существует.
    """
    hashed_password = bcrypt_context.hash(create_user.password)


    new_user = User(name=create_user.name, email=create_user.email, password=hashed_password)

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким адресом электронной почты уже существует"
        )

    return new_user


@router.put('/{user_id}', response_model=ReadUser)
async def update_user(
        user_id: int,
        update_user: CreateUser,
        db: AsyncSession = Depends(get_db)
):
    """
    Обновление данных существующего пользователя.

    Аргументы:
        user_id (int): Идентификатор пользователя.
        update_user (CreateUser): Данные для обновления пользователя.
        db (AsyncSession): Сессия базы данных.

    Возвращает:
        ReadUser: Обновленные данные пользователя.

    Исключения:
        HTTPException: Если пользователь не найден или существует коллизия с адресом электронной почты.
    """
    user = await db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    if update_user.password:
        user.password = bcrypt_context.hash(update_user.password)
    user.name = update_user.name
    user.email = update_user.email

    try:
        db.add(user)
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким адресом электронной почты уже существует"
        )

    return user


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: Annotated[AsyncSession, Depends(get_db)], user_id: int):
    """
    Удаление пользователя по его идентификатору.

    Аргументы:
        db (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя.

    Исключения:
        HTTPException: Если пользователь не найден.
    """
    user = await db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    await db.delete(user)
    await db.commit()

    return
