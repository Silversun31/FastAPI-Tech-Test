from sqlalchemy import Boolean, Column, DateTime, func


class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False)


class TimestampMixin:
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
