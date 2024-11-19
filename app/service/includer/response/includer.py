from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.schema import UserResponse, PostResponse, CommentResponse, TagResponse


class AbstractResponseIncluder(ABC):
    """
    Abstract class that forces the implementation of objects that should follow
    decorator pattern, where schema object is accepted through object
    initialization, and specific property value is populated by calling the
    implementation of attach abstract method.
    """

    def __init__(self, schema: BaseModel) -> None:
        """
        :param schema: Instance of one of the pydantic response models to which
        needs to be decorated with additional data.
        """
        self._schema = schema

    @abstractmethod
    def attach(self, data) -> None:
        """
        Attaches specific relationship property values from given data to
        schema provided through initialization.
        :param data: sqlalchemy model which holds data that needs to be
        attached to provided schema.
        """


class PostsIncluder(AbstractResponseIncluder):
    """Responsible for attaching posts from given data to given schema."""

    def attach(self, data) -> None:
        self._schema.posts = [
            PostResponse.create(post=post)
            for post in data.posts
        ]


class CommentsIncluder(AbstractResponseIncluder):
    """Responsible for attaching comments from given data to given schema."""

    def attach(self, data) -> None:
        self._schema.comments = [
            CommentResponse.create(comment=comment)
            for comment in data.comments
        ]


class TagsIncluder(AbstractResponseIncluder):
    """Responsible for attaching tags from given data to given schema."""

    def attach(self, data) -> None:
        self._schema.tags = [
            TagResponse.create(tag=tag) for tag in data.tags
        ]


class UserIncluder(AbstractResponseIncluder):
    """Responsible for attaching user from given data to given schema."""

    def attach(self, data) -> None:
        self._schema.user = UserResponse.create(user=data.user)
