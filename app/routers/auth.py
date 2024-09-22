from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from app.models.users import User
from app.database.db_session import get_db
from typing import Annotated
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import SECRET_KEY, ALGORITHM, bcrypt_context, oauth2_scheme

router = APIRouter(prefix='/auth', tags=['auth'])


async def authenticate_user(db: Annotated[AsyncSession, Depends(get_db)], username: str, password: str) -> User:
    """
    Аутентификация пользователя, проверка предоставленного имени пользователя и пароля в базе данных.

    Аргументы:
        db (AsyncSession): Сессия базы данных.
        username (str): Имя пользователя, пытающегося пройти аутентификацию.
        password (str): Пароль, предоставленный пользователем.

    Исключения:
        HTTPException: Если учетные данные недействительны.

    Возвращает:
        User: Объект аутентифицированного пользователя.
    """
    user = await db.scalar(select(User).where(User.name == username))
    if not user or not bcrypt_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректные учетные данные",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Получение текущего пользователя на основе JWT токена.

    Аргументы:
        token (str): JWT токен, предоставленный пользователем в заголовке.

    Исключения:
        HTTPException: Если токен недействителен, истёк или отсутствует.

    Возвращает:
        dict: Словарь с данными о пользователе, включая имя и идентификатор.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get('sub')
        user_id: int = payload.get('id')
        expire = payload.get('exp')

        if name is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Не удалось проверить пользователя'
            )
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Не предоставлен токен доступа"
            )
        if datetime.now() > datetime.fromtimestamp(expire):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Токен истёк!"
            )

        return {
            'username': name,
            'id': user_id,
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось проверить пользователя'
        )


async def create_access_token(name: str, user_id: int, expires_delta: timedelta):
    """
    Создание доступа токена для аутентифицированного пользователя.

    Аргументы:
        name (str): Имя пользователя.
        user_id (int): Идентификатор пользователя.
        expires_delta (timedelta): Время жизни токена.

    Возвращает:
        str: JWT токен доступа.
    """
    encode = {'sub': name, 'id': user_id}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.get('/read_current_user')
async def read_current_user(user: dict = Depends(get_current_user)):
    """
    Endpoint для получения данных текущего пользователя.

    Аргументы:
        user (dict): Данные о текущем пользователе, полученные из зависимостей.

    Возвращает:
        dict: Словарь с информацией о пользователе.
    """
    return {'User': user}


@router.post('/token')
async def login(db: Annotated[AsyncSession, Depends(get_db)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Endpoint для получения токена доступа.

    Аргументы:
        db (AsyncSession): Сессия базы данных.
        form_data (OAuth2PasswordRequestForm): Форма с учетными данными пользователя.

    Исключения:
        HTTPException: Если не удалось аутентифицировать пользователя.

    Возвращает:
        dict: Словарь с токеном доступа и типом токена.
    """
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось аутентифицировать пользователя'
        )

    token = await create_access_token(user.name,
                                      user.id,
                                      expires_delta=timedelta(minutes=20))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }
