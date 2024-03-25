import asyncio
import pytest
from httpx import AsyncClient
from core.db import Base, get_db
from app import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import DB_URL

test_engine = create_async_engine(DB_URL)

TestAsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine, class_=AsyncSession
)

# pytest_plugins = "tests.fixtures"


async def override_db():
    """Возвращает соединение с базой данных."""
    async with TestAsyncSessionLocal() as async_session:
        yield async_session


@pytest.fixture(scope="session")
def event_loop(request):

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="function")
async def init_db():

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def client():

    app.dependency_overrides = {get_db: override_db}
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="module")
def save_data() -> dict:
    save_data = {}
    return save_data
