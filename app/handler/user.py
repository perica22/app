from pydantic import UUID4
from fastapi import APIRouter, Request

from app import event
from app.schema import UserResponse
from app.service import UserService
from app.filter import IncludeFilter

router = APIRouter()


@router.get(
    path="/{user_id:uuid}",
    response_model=UserResponse,
    response_model_exclude_none=True,
    summary="Get user details",
    description="Retrieves details of a single user.",
    response_description="Details of a single user."
)
def get_user(
    request: Request,
    user_id: UUID4,
    include_filter: IncludeFilter = IncludeFilter.inject()
) -> UserResponse:
    user = UserService(
        db=request.state.db,
    ).get_user(
        user_id=str(user_id),
        include=include_filter.value
    )

    request.state.audit(event=event.GET_USER)
    return user
