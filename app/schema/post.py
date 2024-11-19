from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel, UUID4

if TYPE_CHECKING:
    from app.schema.user import UserResponse
from app.db import Post
from app.schema.comment import CommentResponse
from app.schema.tag import TagResponse


class PostResponse(BaseModel):
    id: UUID4
    title: str
    content: str
    status: str
    user: Optional["UserResponse"] = None
    comments: Optional[list[CommentResponse]] = None
    tags: Optional[list[TagResponse]] = None

    @classmethod
    def create(cls, post: Post) -> "PostResponse":
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            status=post.status
        )
