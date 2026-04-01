from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr
    password: str
    repeat_password: str

    @field_validator('password')
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not any(c.isdigit() for c in v):
                raise ValueError("Password must contain at least one digit")
            if v.islower():
                raise ValueError("Password must contain one uppercase sym")
            if not set('!@#$%&*').intersection(v):
                raise ValueError(
                    "Password must contain at least one symbol like(! @ # $ % & *)" # noqa
                )
            return v

    @field_validator('repeat_password')
    def passwords_match(cls, v, info):
        if v is not None and 'password' in info.data:
            if v != info.data.get('password'):
                raise ValueError('Passwords do not match')
        return v


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    repeat_password: str | None = None

    @field_validator('password')
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not any(c.isdigit() for c in v):
                raise ValueError("Password must contain at least one digit")
            if v.islower():
                raise ValueError("Password must contain one uppercase sym")
            if not set('!@#$%&*').intersection(v):
                raise ValueError(
                    "Password must contain at least one symbol like(! @ # $ % & *)" # noqa
                )
            return v

    @field_validator('repeat_password')
    def passwords_match(cls, v, info):
        if v is not None and 'password' in info.data:
            if v != info.data.get('password'):
                raise ValueError('Passwords do not match')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserToken(BaseModel):
    token: str
