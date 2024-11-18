from pydantic import BaseModel, UUID4

from app.db import Post


class PostResponse(BaseModel):
    id: UUID4
    title: str
    content: str
    status: str

    @classmethod
    def create(cls, post: Post) -> 'PostResponse':
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            status=post.status
        )
