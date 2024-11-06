from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from .mixins import SoftDeleteMixin, TimestampMixin
from .post import post_tag


class Tag(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    posts = relationship('Post', secondary=post_tag, back_populates='tags')
