from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.db import Base
from app.database.db_session import get_db
import uuid

# SQLite database URL for testing
SQLITE_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"
unique_email = f"user_{uuid.uuid4()}@example.com"

# Create a SQLAlchemy async engine
engine = create_async_engine(
    SQLITE_DATABASE_URL,
    future=True,
    echo=True,
)

# Create a sessionmaker to manage async sessions
TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Create tables in the database
@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """Настройка базы данных и создание таблиц."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db():
    """Создание новой сессии базы данных для теста."""
    async with TestingSessionLocal() as session:
        yield session
        await session.commit()

@pytest.fixture
async def user_payload():
    return {
        "name": "testuser",
        "email": unique_email,
        "password": "securepassword",
    }

@pytest.fixture
async def test_client(db):
    """Создание TestClient для приложения FastAPI."""
    app.dependency_overrides[get_db] = lambda: db  # Переопределение зависимости базы данных
    async with AsyncClient(app=app) as client:
        yield client
