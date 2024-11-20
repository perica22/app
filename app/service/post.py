import logging
from typing import Optional

from sqlalchemy.orm.session import Session

from app import errors
from app.db import Post, PostStatusType
from app.schema import PostResponse
from app.service.includer.query import PostQueryIncluderFactory
from app.service.includer.response import ResponseIncluderFactory
from app.enum import PostIncludeFilter

logger = logging.getLogger(__name__)


class PostService:
    """Class holds all post related operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_post(
        self, post_id: str, include: list[PostIncludeFilter]
    ) -> PostResponse:
        """
        Method will fetch post with provided `post_id`, with all relationships
        joined that are requested through `include`.
        """
        query_includer_factory = PostQueryIncluderFactory(include=include)
        post = Post.get(
            db=self.db,
            post_id=post_id,
            query_includer_factory=query_includer_factory
        )
        if post is None:
            raise errors.PostNotFound()

        post_schema = PostResponse.create(post=post)
        for incl in ResponseIncluderFactory(include=include):
            incl(schema=post_schema).attach(data=post)

        return post_schema

    def list_posts(
        self,
        include: list[PostIncludeFilter],
        status: Optional[PostStatusType] = None
    ) -> list[PostResponse]:
        """
        Method will fetch all posts, with all relationships joined that are
        requested through `include`. If `status` is provided, only posts with
        given status will be returned.
        """
        query_incl_factory = PostQueryIncluderFactory(include=include)
        posts = Post.list(
            db=self.db,
            status=status,
            query_includer_factory=query_incl_factory
        )
        posts_schema = []
        for post in posts:
            post_schema = PostResponse.create(post=post)
            for incl in ResponseIncluderFactory(include=include):
                incl(schema=post_schema).attach(data=post)
            posts_schema.append(post_schema)

        return posts_schema
