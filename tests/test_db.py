from dataclasses import asdict
from sqlalchemy import select

import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_proj.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(
            new_user
        )  # Não precisa do await pois não existe IO, está apenas alocando na memória
        await session.commit()

        user = await session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
