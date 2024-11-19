from typing import Optional

from pydantic import BaseModel, UUID4

from app.db import User
from app.schema.post import PostResponse
from app.schema.comment import CommentResponse


class UserResponse(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: str
    posts: Optional[list["PostResponse"]] = None
    comments: Optional[list["CommentResponse"]] = None

    @classmethod
    def create(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )
