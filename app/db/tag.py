from uuid import uuid4
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String, Table, ForeignKey

from app.db import Base


# Association Table for the Many-to-Many relationship between Posts and Tags
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column(
        "post_id",
        UUID(as_uuid=True),
        ForeignKey("posts.id"),
        primary_key=True
    ),
    Column(
        "tag_slug",
        String,
        ForeignKey("tags.slug"),
        primary_key=True
    )
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), default=uuid4, primary_key=True)
    slug = Column(String(100), index=True, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")
