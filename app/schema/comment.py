from pydantic import BaseModel, UUID4

from app.db import Comment


class CommentResponse(BaseModel):
    id: UUID4
    content: str

    @classmethod
    def create(cls, comment: Comment) -> 'CommentResponse':
        return cls(
            id=comment.id,
            content=comment.content,
        )
