from enum import Enum


class UserIncludeFilter(Enum):
    POSTS = "POSTS"
    COMMENTS = "COMMENTS"


class PostIncludeFilter(Enum):
    USER = "USER"
    TAGS = "TAGS"
    COMMENTS = "COMMENTS"
