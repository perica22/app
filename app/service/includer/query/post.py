from sqlalchemy.orm.query import Query
from sqlalchemy.orm import subqueryload

from app.db import Post
from app.service.includer.query.base import QueryIncluderInterface


class UserToPostQueryIncluder(QueryIncluderInterface):

    def apply(self, query: Query) -> Query:
        """Joins user details to post from provided query."""
        return query.options(
            subqueryload(
                Post.user
            )
        )


class CommentsToPostQueryIncluder(QueryIncluderInterface):

    def apply(self, query: Query) -> Query:
        """Joins all comments that are related to post from provided query."""
        return query.options(
            subqueryload(
                Post.comments
            )
        )


class TagsToPostQueryIncluder(QueryIncluderInterface):

    def apply(self, query: Query) -> Query:
        """Joins all tags that are related to post from provided query."""
        return query.options(
            subqueryload(
                Post.tags
            )
        )
