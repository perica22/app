import logging

from sqlalchemy.orm.session import Session

from app import errors
from app.db import User
from app.schema import UserResponse

logger = logging.getLogger(__name__)


class UserService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, user_id: str) -> UserResponse:
        user = User.get(db=self.db, user_id=user_id)
        if user is None:
            raise errors.UserNotFound()
        return UserResponse.create(
            user=user
        )
