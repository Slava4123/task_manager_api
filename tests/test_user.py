import pytest
from httpx import ASGITransport, AsyncClient
from pprint import pprint

from app.main import app


@pytest.fixture
def invalid_user_payload():
    return {
        "name": "",  # Отсутствующее имя пользователя
        "email": "invalid-email",
        "password": "short"  # Слишком короткий пароль
    }

@pytest.mark.asyncio
async def test_create_user(test_client: AsyncClient, user_payload: dict):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Sending payload:", user_payload)
        response = await ac.post("/users", json=user_payload)

        print("Response:", response.json())
        assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_user_missing_data(test_client: AsyncClient, invalid_user_payload: dict):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Sending invalid payload:", invalid_user_payload)
        response = await ac.post("/users", json=invalid_user_payload)

        print("Response:", response.json())
        assert response.status_code == 422  # Ожидаем статус код 422 для некорекотной схемы
        assert "detail" in response.json()  # Проверяем наличие поля detail в ответе


@pytest.mark.asyncio
async def test_create_user_duplicate(test_client: AsyncClient, user_payload: dict):
    # Сначала создаем пользователя
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/users", json=user_payload)

    # Затем пробуем создать его повторно
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Trying to create duplicate user:", user_payload)
        response = await ac.post("/users", json=user_payload)

        print("Response:", response.json())
        assert response.status_code == 400  # Ожидаем конфликт при создании дубликата