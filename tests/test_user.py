import pytest
from httpx import ASGITransport, AsyncClient

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
        assert response.json()["name"] == user_payload["name"]
        assert response.json()["email"] == user_payload["email"]


@pytest.mark.asyncio
async def test_create_user_missing_data(test_client: AsyncClient, invalid_user_payload: dict):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        print("Sending invalid payload:", invalid_user_payload)
        response = await ac.post("/users", json=invalid_user_payload)

        print("Response:", response.json())
        assert response.status_code == 422
        assert "detail" in response.json()


@pytest.mark.asyncio
async def test_create_user_duplicate(test_client: AsyncClient, user_payload: dict):
    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        await ac.post("/users", json=user_payload)

    async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/users", json=user_payload)

        assert response.status_code == 400
