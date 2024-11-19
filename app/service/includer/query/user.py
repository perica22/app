from sqlalchemy.orm.query import Query
from sqlalchemy.orm import subqueryload

from app.db import User
from app.service.includer.query.base import QueryBuilderInterface


class PostsToUserQueryBuilder(QueryBuilderInterface):

    def apply(self, query: Query) -> Query:
        """Joins all posts that are related to user from provided query."""
        return query.options(
            subqueryload(
                User.posts
            )
        )


class CommentsToUserQueryBuilder(QueryBuilderInterface):

    def apply(self, query: Query) -> Query:
        """Joins all comments that are related to user from provided query."""
        return query.options(
            subqueryload(
                User.comments
            )
        )
