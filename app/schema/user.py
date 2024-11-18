from pydantic import BaseModel, UUID4

from app.db import User


class UserResponse(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: str

    @classmethod
    def create(cls, user: User) -> 'UserResponse':
        return cls(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
