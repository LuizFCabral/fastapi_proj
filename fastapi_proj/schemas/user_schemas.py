from pydantic import BaseModel, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserPass(UserSchema):
    password: str = Field(..., min_length=6)


class UserResponseSchema(UserSchema):
    id: int


class UsersList(BaseModel):
    users: list[UserResponseSchema]
