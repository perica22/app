import logging

from sqlalchemy.orm.session import Session

from app import errors
from app.db import Post
from app.schema import PostResponse

logger = logging.getLogger(__name__)


class PostService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_post(self, post_id: str) -> PostResponse:
        post = Post.get(db=self.db, post_id=post_id)
        if post is None:
            raise errors.PostNotFound()
        return PostResponse.create(
            post=post
        )

    def list_posts(self) -> list[PostResponse]:
        posts = Post.list(db=self.db)
        return [
            PostResponse.create(post=post) for post in posts
        ]
