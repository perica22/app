from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, ForeignKey, Text

from app.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    post_id = Column(
        UUID(as_uuid=True),
        ForeignKey("posts.id"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
