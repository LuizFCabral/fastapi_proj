from http import HTTPStatus
from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


from fastapi_proj.database import get_session
from fastapi_proj.models import User
from fastapi_proj.schemas.user_schemas import Message
from fastapi_proj.schemas.user_schemas import (
    UserSchema,
    UserPublic,
    UsersList,
)

app = FastAPI(title='Test Infog')


def user_exists(user_id, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return db_user


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def register_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='Username already exists', status_code=HTTPStatus.CONFLICT
            )
        if db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/user/', status_code=HTTPStatus.OK, response_model=UsersList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get('/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_id(user_id: int, session: Session = Depends(get_session)):
    user = user_exists(user_id, session)

    return user


@app.put('/user/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db = user_exists(user_id, session)

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password

    try:
        session.add(user_db)
        session.commit()
        session.refresh(user_db)
        return user_db
    except IntegrityError:
        raise HTTPException(
            detail='User name or email already exists', status_code=HTTPStatus.CONFLICT
        )


@app.delete('/user/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = user_exists(user_id, session)

    session.delete(user_db)
    session.commit()

    return {'message': 'User deleted'}
