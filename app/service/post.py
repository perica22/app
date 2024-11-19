import logging
from typing import Optional

from sqlalchemy.orm.session import Session

from app import errors
from app.db import Post, PostStatusType
from app.schema import PostResponse
from app.service.includer.query import PostQueryBuilderFactory
from app.service.includer.response import ResponseIncluderFactory

logger = logging.getLogger(__name__)


class PostService:

    def __init__(self, db: Session) -> None:
        self.db = db

    def get_post(self, post_id: str, include: list[str]) -> PostResponse:
        query_builder_factory = PostQueryBuilderFactory(include=include)
        post = Post.get(
            db=self.db,
            post_id=post_id,
            query_builder_factory=query_builder_factory
        )
        if post is None:
            raise errors.PostNotFound()

        post_schema = PostResponse.create(post=post)
        for incl in ResponseIncluderFactory(query_builder_factory.include):
            incl(schema=post_schema).attach(data=post)

        return post_schema

    def list_posts(
        self,
        include: list[str],
        status: Optional[PostStatusType] = None
    ) -> list[PostResponse]:
        query_builder_factory = PostQueryBuilderFactory(include=include)
        posts = Post.list(
            db=self.db,
            status=status,
            query_builder_factory=query_builder_factory
        )
        posts_schema = []
        for post in posts:
            post_schema = PostResponse.create(post=post)
            for incl in ResponseIncluderFactory(query_builder_factory.include):
                incl(schema=post_schema).attach(data=post)
            posts_schema.append(post_schema)

        return posts_schema
