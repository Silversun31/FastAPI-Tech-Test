from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional
from datetime import datetime


class UserLogin(BaseModel):
    username: constr(max_length=20)
    password: str


class UserBase(BaseModel):
    username: constr(max_length=20)
    email: Optional[EmailStr] = Field(default=None)


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
