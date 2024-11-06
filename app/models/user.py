from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from .mixins import SoftDeleteMixin, TimestampMixin


class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship('Post', back_populates='owner', lazy="selectin")
    comments = relationship('Comment', back_populates='owner', lazy="selectin")
