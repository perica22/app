from typing import Any
from enum import Enum

from fastapi import Query, Depends

from app import errors
from app.db import PostStatusType


class PostStatusFilter:
    """
    This filter will be used for filtering posts using status value from
    query parameter.
    """
    STATUS_QUERY = Query(
        default=None,
        description="Filter by post current status",
        examples=["draft", "active"],
    )

    def __call__(self, status: str = STATUS_QUERY) -> "PostStatusFilter":
        # check if provided status filter is valid
        if not status:
            self.value = None
        elif status.upper() not in PostStatusType.all():
            raise errors.InvalidPostStatus()
        else:
            self.value = PostStatusType[status.upper()]
        return self

    @classmethod
    def inject(cls) -> Any:
        return Depends(cls())


class IncludeFilter:
    """
    This filter will be used for controlling content of http response, by
    allowing clients to request some related entities to be included in the
    response.
    """
    INCLUDE_QUERY = Query(
        default=None,
        description=(
            "Request additional entities to be included in the response"
        ),
        examples=["comments,tags", "tags", "user"],
    )

    def __init__(self, entity: type[Enum]) -> None:
        self.entity = entity

    def __call__(self, include: str = INCLUDE_QUERY) -> "IncludeFilter":
        """
        Parses the string of include values and validates if each of them is
        supported by checking its existence in provide enum through object
        initialization.
        """
        values = set(include.split(",")) if include is not None else set()
        try:
            self.value = [self.entity(value.upper()) for value in values]
        except ValueError:
            raise errors.InvalidIncludeValue()
        return self

    @classmethod
    def inject(cls, entity: type[Enum]) -> Any:
        return Depends(cls(entity=entity))
