from enum import Enum
from collections.abc import Iterable

from app.service.includer.response.includer import (
    AbstractResponseIncluder, CommentsIncluder, UserIncluder,
    TagsIncluder, PostsIncluder
)


class ResponseIncluderFactory:
    """
    ResponseIncluder factory that accepts include values through
    initialization and behaves like Iterable, producing ResponseIncluder
    objects for each include value provided using includer_map attribute.
    """
    response_includer_map: dict[str, AbstractResponseIncluder] = {
        "POSTS": PostsIncluder,
        "COMMENTS": CommentsIncluder,
        "USER": UserIncluder,
        "TAGS": TagsIncluder,
    }

    def __init__(self, include: Iterable[Enum]) -> None:
        self._include = include

    def __iter__(self) -> Iterable[type[AbstractResponseIncluder]]:
        for incl in self._include:
            yield self.response_includer_map[incl.value]
