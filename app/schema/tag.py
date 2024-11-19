from pydantic import BaseModel, UUID4

from app.db import Tag


class TagResponse(BaseModel):
    id: UUID4
    slug: str

    @classmethod
    def create(cls, tag: Tag) -> 'TagResponse':
        return cls(
            id=tag.id,
            slug=tag.slug,
        )
