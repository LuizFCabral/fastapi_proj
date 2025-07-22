from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_proj.database import engine, get_session
from fastapi_proj.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'test')
        )

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }


@pytest.mark.asyncio
async def test_get_session():
    gen = get_session()

    # Verifica se é um gerador assíncrono
    assert hasattr(gen, '__aiter__')

    # Obtém a sessão do gerador
    session = await anext(gen)

    assert isinstance(session, AsyncSession)
    assert session.bind is engine
    assert session.is_active  # Deve estar ativa durante o uso
