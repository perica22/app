import enum
from uuid import uuid4
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String, ForeignKey, Text, Enum

from app.db import Base
from app.db.tag import post_tags


class PostStatusType(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

    @classmethod
    def all(cls):
        return {status.value for status in cls}


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)
    status = Column(
        Enum(PostStatusType), nullable=False, default=PostStatusType.DRAFT
    )

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", lazy="raise")
    tags = relationship(
        "Tag", secondary=post_tags, back_populates="posts", lazy="raise"
    )

    @classmethod
    def get(cls, db: Session, post_id: str) -> 'Post':
        query = db.query(cls).filter_by(
            id=post_id
        )
        return query.one_or_none()

    @classmethod
    def list(
        cls, db: Session, status: Optional[PostStatusType] = None
    ) -> list['Post']:
        query = db.query(cls)
        if status:
            query = query.filter_by(status=status)
        return query.all()
