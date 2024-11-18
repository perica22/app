from tests.testing.precondition.models import (
    UserMockPrecondition, PostMockPrecondition, CommentMockPrecondition,
    TagMockPrecondition
)


class Precondition:
    """
    Base class for mock precondition. Every component precondition class should
    inherit this class.
    """
    def __init__(self, mocks=None):
        self.mocks = mocks


class ConfigPrecondition(Precondition):
    def __init__(self, mocks):
        super().__init__(mocks)
        self.config = mocks.config


class ModelPrecondition(Precondition):
    def __init__(self, mocks):
        self.user = UserMockPrecondition()
        self.post = PostMockPrecondition()
        self.comment = CommentMockPrecondition()
        self.tag = TagMockPrecondition()
        super().__init__(mocks)


class AppPrecondition(ConfigPrecondition, ModelPrecondition):
    def __init__(self, mocks):
        super().__init__(mocks)
