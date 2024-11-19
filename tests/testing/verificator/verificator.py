from tests.testing.verificator.http import HttpVerificator
from tests.testing.verificator.models import (
    UserVerificator, PostVerificator, TagVerificator, CommentVerificator
)
from tests.testing.verificator.base import Verificator


class ModelVerificator(Verificator):
    def __init__(self, mocks):
        self.user = UserVerificator()
        self.post = PostVerificator()
        self.comment = CommentVerificator()
        self.tag = TagVerificator()
        super().__init__(mocks)


class AppVerificator(HttpVerificator, ModelVerificator):
    def __init__(self, mocks, **kwargs):
        super().__init__(mocks, **kwargs)
