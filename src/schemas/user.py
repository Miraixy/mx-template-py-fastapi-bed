from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int #  # noqa: A003
    username: str
    password: str
    perm_level: int
    login_time: datetime

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str
    perm_level: int
    access_key: str


class UserUpdate(BaseModel):
    access_key: str
    username: str
    perm_level: int


class UserLogin(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: str
