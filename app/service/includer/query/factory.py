from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.service.includer.query.base import QueryIncluderInterface
from app.service.includer.query.post import (
    UserToPostQueryIncluder, CommentsToPostQueryIncluder,
    TagsToPostQueryIncluder
)
from app.service.includer.query.user import (
    PostsToUserQueryIncluder, CommentsToUserQueryIncluder
)


class AbstractQueryIncluderFactory(ABC):
    """
    Abstract QueryIncluder factory object that accepts include values through
    initialization and behaves like Iterable, producing QueryIncluder objects
    for each include value provided from query_includer_map abstract method.
    """
    def __init__(self, include: list[str]) -> None:
        self.include = set(include).intersection(
            set(self.query_includer_map.keys())
        )

    def __iter__(self) -> Iterable[QueryIncluderInterface]:
        """
        Yields correct QueryIncluder object for each include value provided.
        """
        for value in self.include:
            yield self.query_includer_map[value]()

    @property
    @abstractmethod
    def query_includer_map(self) -> dict[str, type[QueryIncluderInterface]]:
        """
        Abstract property that should return map with each supported include
        filter value as key and specific QueryIncluder that holds correct build
        implementation.
        """


class PostQueryIncluderFactory(AbstractQueryIncluderFactory):
    """Factory for Post model relationships."""

    query_includer_map = {
        "user": UserToPostQueryIncluder,
        "comments": CommentsToPostQueryIncluder,
        "tags": TagsToPostQueryIncluder
    }


class UserQueryIncluderFactory(AbstractQueryIncluderFactory):
    """Factory for User model relationships."""

    query_includer_map = {
        "posts": PostsToUserQueryIncluder,
        "comments": CommentsToUserQueryIncluder
    }
