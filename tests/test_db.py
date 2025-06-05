from sqlalchemy import select

from fastapi_proj.models import User


def test_create_user(session):
    new_user = User(username='test', email='test@test', password='secret')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.username == 'test'
