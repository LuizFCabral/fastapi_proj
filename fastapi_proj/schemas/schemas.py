from pydantic import BaseModel, EmailStr, Field, ConfigDict


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
    offset: int = (0,)
    limit: int = 10
