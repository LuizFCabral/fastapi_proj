import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from datetime import datetime
from contextlib import contextmanager
from sqlalchemy.pool import StaticPool

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from fastapi_proj.app import app
from fastapi_proj.models import User, table_registry
from fastapi_proj.database import get_session
from fastapi_proj.setting import Settings
from fastapi_proj.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn: 
        await conn.run_sync(table_registry.metadata.create_all) 

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(table_registry.metadata.drop_all)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 6, 26)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'testtest'
    user = User(
        username='teste', email='test@example.com', password=get_password_hash(password)
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': user.clean_password}
    )

    return response.json()['access_token']


@pytest.fixture
def settings():
    return Settings()
