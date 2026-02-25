import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from httpx import AsyncClient

from app.main import create_app
from app.database import Base
from app.models.timer import Timer, TimerEvent


@pytest_asyncio.fixture
async def test_engine():
    """Create in-memory SQLite async engine for tests."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session_factory(test_engine):
    """Create async session factory for tests."""
    return async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )


@pytest_asyncio.fixture
async def test_session(test_session_factory):
    """Create test database session."""
    async with test_session_factory() as session:
        yield session


@pytest_asyncio.fixture
async def test_app(test_session_factory, monkeypatch):
    """Create FastAPI test app with overridden database dependency."""
    app = create_app()
    
    async def override_get_db():
        async with test_session_factory() as session:
            yield session
    
    from app.database import get_db
    app.dependency_overrides[get_db] = override_get_db
    
    yield app
    
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_client(test_app):
    """Create AsyncClient for testing FastAPI endpoints."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop_policy():
    """Use default event loop policy for async tests."""
    import asyncio
    return asyncio.get_event_loop_policy()
