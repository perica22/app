import logging

from sqlalchemy.orm.session import Session

from app import errors
from app.db import User
from app.schema import UserResponse
from app.service.includer.query import UserQueryIncluderFactory
from app.service.includer.response import ResponseIncluderFactory

logger = logging.getLogger(__name__)


class UserService:
    """Class holds all user related operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_user(self, user_id: str, include: list[str]) -> UserResponse:
        """
        Method will fetch user with provided `user_id`, with all relationships
        joined that are requested through `include`.
        """
        query_incl_factory = UserQueryIncluderFactory(include=include)
        user = User.get(
            db=self.db,
            user_id=user_id,
            query_includer_factory=query_incl_factory
        )
        if user is None:
            raise errors.UserNotFound()

        user_schema = UserResponse.create(user=user)
        for includer in ResponseIncluderFactory(query_incl_factory.include):
            includer(schema=user_schema).attach(data=user)
        return user_schema
