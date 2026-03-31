from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    repeat_password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    repeat_password: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    repeat_password: str


class UserToken(BaseModel):
    token: str
