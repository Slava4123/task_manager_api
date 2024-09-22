import os
from datetime import timedelta, datetime
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Any, Dict, Annotated
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
load_dotenv()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret')  # Убедитесь, что вы импортируете os
ALGORITHM = 'HS256'
def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:

    """
    Создает JWT токен доступа.
    Параметры:
    - data (Dict[str, Any]): Данные, которые будут включены в токен.
    - expires_delta (timedelta | None): Опциональное время жизни токена.
      Если не указано, используется значение по умолчанию (15 минут).
    Возвращает:
    - str: Закодированный JWT токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)  # Стандартное время жизни токена 15 минут
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
def verify_access_token(token: str) -> Dict[str, Any]:
    """
    Проверяет и декодирует JWT токен.
    Параметры:
    - token (str): JWT токен для проверки и декодирования.
    Возвращает:
    - Dict[str, Any]: Декодированные данные токена, если он действителен.
    - None: Если токен недействителен.
    """
    if not token:
        raise ValueError("Токен не может быть пустым")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise ValueError("Недействительный токен")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Извлекает текущего пользователя из токена доступа.
    Параметры:
    - token (str): JWT токен доступа, полученный из заголовков запроса.
    Возвращает:
    - Dict[str, Any]: Информация о пользователе, включая имя пользователя и идентификатор.
    Исключения:
    - HTTPException: Если токен недействителен или истек.
    """
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    name: str = payload.get('sub')
    user_id: int = payload.get('id')
    expire = payload.get('exp')
    if name is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )
    if expire is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token supplied"
        )
    if datetime.now() > datetime.fromtimestamp(expire):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token expired!"
        )
    return {
        'username': name,
        'id': user_id,
    }
async def generate_access_token(name: str, user_id: int, expires_delta: timedelta | None = None):
    """
    Генерирует токен доступа для указанного пользователя.
    Параметры:
    - name (str): Имя пользователя.
    - user_id (int): Уникальный идентификатор пользователя.
    - expires_delta (timedelta | None): Опциональное время жизни токена.
    Возвращает:
    - str: Сгенерированный JWT токен.
    """
    data = {"sub": name, "id": user_id}  # добавляем данные в токен
    return create_access_token(data, expires_delta)