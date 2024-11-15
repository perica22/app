import enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String, ForeignKey, Text, Enum

from app.db import Base
from app.db.tag import post_tags


class PostStatusType(enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


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
