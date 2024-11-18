from typing import Any

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
