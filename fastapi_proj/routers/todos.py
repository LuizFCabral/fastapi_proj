from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_proj.database import get_session
from fastapi_proj.models import Todo, User
from fastapi_proj.schemas.schemas import (
    FilterTodo,
    TodoList,
    TodoPublic,
    TodoSchema,
)
from fastapi_proj.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=TodoPublic)
async def create_todo(todo: TodoSchema, session: Session, user: CurrentUser):
    db_todo = Todo(
        user_id=user.id,
        title=todo.title,
        description=todo.description,
        state=todo.state,
    )

    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)

    return db_todo


@router.get('/', status_code=HTTPStatus.OK, response_model=TodoList)
async def list_todos(
    session: Session,
    user: CurrentUser,
    todo_filter: Annotated[FilterTodo, Query()],
):
    query = select(Todo).where(Todo.user_id == user.id)

    if todo_filter.title:
        query = query.filter(Todo.title.contains(todo_filter.title))

    if todo_filter.description:
        query = query.filter(
            Todo.description.contains(todo_filter.description)
        )

    if todo_filter.state:
        query = query.filter(Todo.state == todo_filter.state)

    todos = await session.scalars(
        query.limit(todo_filter.limit).offset(todo_filter.offset)
    )

    return {'todos': todos}
