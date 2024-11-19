from uuid import uuid4
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, DateTime, String

from app.db import Base
if TYPE_CHECKING:
    from app.service.includer.query import UserQueryBuilderFactory


class User(Base):

    __tablename__ = "users"
    # TODO
    # __table_args__ = (
    #     Index),
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
    def get(
        cls,
        db: Session,
        user_id: str,
        query_builder_factory: "UserQueryBuilderFactory"
    ) -> "User":
        query = db.query(cls).filter_by(
            id=user_id
        )
        for qb in query_builder_factory:
            query = qb.apply(query)

        return query.one_or_none()
