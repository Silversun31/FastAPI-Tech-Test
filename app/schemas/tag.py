from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    name: Optional[str]


class Tag(TagBase):
    id: int
    name: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
