from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String

from app.db import Base


class User(Base):

    __tablename__ = "users"
    # __table_args__ = (
    #     Index("user_tenant_index", "user_id", "tenant_id"),
    # )

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    created_at = Column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)

    posts = relationship("Post", back_populates="user", lazy="raise")
    comments = relationship("Comment", back_populates="user", lazy="raise")

    @classmethod
    def get(cls, db: Session, user_id: str) -> 'User':
        query = db.query(cls).filter_by(
            id=user_id
        )
        return query.one_or_none()
