import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.database import Base, get_session
from app.config import get_settings


@pytest.fixture(scope="session")
def event_loop_policy():
    """Set event loop policy for async tests."""
    import asyncio
    if asyncio.sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.get_event_loop_policy()


@pytest_asyncio.fixture
async def test_db_engine():
    """Create test database engine."""
    settings = get_settings()
    test_db_url = settings.database_url.replace(
        "postgresql://", "postgresql+asyncpg://"
    ).replace("timers", "timers_test")
    
    engine = create_async_engine(
        test_db_url,
        echo=False,
        pool_pre_ping=True,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_session(test_db_engine):
    """Create test database session."""
    async_session_factory = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(test_db_session):
    """Create test HTTP client with overridden database dependency."""
    async def override_get_session():
        yield test_db_session
    
    app.dependency_overrides[get_session] = override_get_session
    
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def anyio_backend():
    """Configure anyio backend for async tests."""
    return "asyncio"
