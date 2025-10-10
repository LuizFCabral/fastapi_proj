from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fastapi_proj.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserPublic(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    id: int
    model_config = ConfigDict(from_attributes=True)


class UsersList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=10)


class FilterTodo(FilterPage):
    title: str | None = Field(default=None, min_length=3)
    description: str | None = None
    state: TodoState | None = None


class TodoSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=300)
    state: TodoState = Field(default=TodoState.todo)


class TodoPublic(TodoSchema):
    id: int


class TodoList(TodoPublic):
    todos: list[TodoPublic]
