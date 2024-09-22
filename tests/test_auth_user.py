
import pytest
from httpx import AsyncClient
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.main import app
from app.models.users import User
from app.database.db_session import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@pytest.fixture
async def access_token(client, test_user):
    response = await client.post("/auth/token", data={
        "username": test_user.name,
        "password": "testpassword"
    })
    assert response.status_code == 200
    token = response.json().get("access_token")
    return token

@pytest.fixture(scope='function')
async def db_session() -> AsyncSession:
    db_gen = get_db()
    async for session in db_gen:
        try:
            yield session
        finally:
            await session.close()

@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession):
    user = User(name="testuser", password=get_password_hash('testpassword'),
                email="testuser@mail.com")

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    yield user  # Возвращаем созданного пользователя для тестов

    try:
        await db_session.delete(user)
        await db_session.commit()
    except Exception:
        await db_session.rollback()  # Откат при возникновении ошибки
        raise  # Повторное поднятие исключения для дальнейшей обработки
    finally:
        await db_session.rollback()

@pytest.fixture(scope="module")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_user: User):
    response = await client.post("/auth/token", data={
        "username": test_user.name,
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_read_current_user_without_token(client: AsyncClient):
    response = await client.get("/auth/read_current_user")
    assert response.status_code == 401  # 401 Unauthorized

@pytest.mark.asyncio
async def test_read_current_user_with_token(client: AsyncClient, test_user: User, access_token):
    response = await client.get("/auth/read_current_user", headers={"Authorization": f"Bearer {access_token}"})
    data = response.json()
    assert "username" in data["User"]
    assert data["User"]["username"] == test_user.name
    assert response.status_code == status.HTTP_200_OK


