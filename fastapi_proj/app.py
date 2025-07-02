from http import HTTPStatus
from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy import select


from fastapi_proj.database import get_session
from fastapi_proj.models import User
from fastapi_proj.schemas.user_schemas import Message
from fastapi_proj.schemas.user_schemas import (
    UserPass,
    UserResponseSchema,
    UsersList,
)

app = FastAPI(title='Test Infog')

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá mundo!'}


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserResponseSchema)
def register_user(user: UserPass, session=Depends(get_session)):
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

    # user_with_id = UserResponseSchema(**user.model_dump(), id=len(database) + 1)
    # database.append(user_with_id)
    # return user_with_id


@app.get('/user/', status_code=HTTPStatus.OK, response_model=UsersList)
def read_users(session=Depends(get_session)):
    users = session.scalars(select(User))
    return {'users': users}


@app.get(
    '/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserResponseSchema
)
def read_user_id(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user = database[user_id - 1]
    user_with_id = UserResponseSchema(**user.model_dump())
    return user_with_id


@app.put('/user/{user_id}', response_model=UserResponseSchema)
def update_user(user_id: int, user: UserPass):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_with_id = UserResponseSchema(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/user/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del database[user_id - 1]

    return {'message': 'User deleted'}
