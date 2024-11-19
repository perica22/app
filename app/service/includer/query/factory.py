from abc import ABC, abstractmethod

from app.service.includer.query.base import QueryBuilderInterface
from app.service.includer.query.post import (
    UserToPostQueryBuilder, CommentsToPostQueryBuilder, TagsToPostQueryBuilder
)
from app.service.includer.query.user import (
    PostsToUserQueryBuilder, CommentsToUserQueryBuilder
)


class AbstractQueryBuilderFactory(ABC):
    """
    Abstract QueryBuilder factory object that accepts include values through
    initialization and behaves like Iterable, producing QueryBuilder objects
    for each include value provided using query_builder_map abstract method.
    """
    def __init__(self, include: list[str]) -> None:
        self.include = set(include).intersection(
            set(self.query_builder_map.keys())
        )

    def __iter__(self) -> QueryBuilderInterface:
        """
        Yields correct QueryBuilder object for each include value provided.
        """
        for value in self.include:
            yield self.query_builder_map[value]()

    @property
    @abstractmethod
    def query_builder_map(self) -> dict[str, type[QueryBuilderInterface]]:
        """
        Abstract property that should return map with each supported include
        filter value as key and specific QueryBuilder that holds correct build
        implementation.
        """


class PostQueryBuilderFactory(AbstractQueryBuilderFactory):
    """Factory for Post model relationships."""

    query_builder_map = {
        "user": UserToPostQueryBuilder,
        "comments": CommentsToPostQueryBuilder,
        "tags": TagsToPostQueryBuilder
    }


class UserQueryBuilderFactory(AbstractQueryBuilderFactory):
    """Factory for User model relationships."""

    query_builder_map = {
        "posts": PostsToUserQueryBuilder,
        "comments": CommentsToUserQueryBuilder
    }
