from pydantic import BaseModel, UUID4

from app.db import Comment


class CommentResponse(BaseModel):
    id: UUID4
    post_id: UUID4
    user_id: UUID4
    content: str

    @classmethod
    def create(cls, comment: Comment) -> "CommentResponse":
        return cls(
            id=comment.id,
            content=comment.content,
            user_id=comment.user_id,
            post_id=comment.post_id
        )
