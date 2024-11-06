from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from .mixins import SoftDeleteMixin, TimestampMixin


class Comment(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='comments')
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='comments')
