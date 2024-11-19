from app.service.includer.response.includer import (
    AbstractResponseIncluder, PostIncluder, CommentsIncluder, UserIncluder,
    TagsIncluder, PostsIncluder
)


class ResponseIncluderFactory:
    """
    ResponseIncluder factory that accepts include values through
    initialization and behaves like Iterable, producing ResponseIncluder
    objects for each include value provided using includer_map attribute.
    """
    includer_map: dict[str, AbstractResponseIncluder] = {
        "posts": PostsIncluder,
        "comments": CommentsIncluder,
        "user": UserIncluder,
        "tags": TagsIncluder,
        "post": PostIncluder
    }

    def __init__(self, include: set[str]) -> None:
        self._include = include

    def __iter__(self) -> type[AbstractResponseIncluder]:
        for incl in self._include:
            yield self.includer_map[incl]
