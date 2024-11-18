from pydantic import UUID4
from fastapi import APIRouter, Request

from app import event
from app.schema import UserResponse
from app.service import UserService

router = APIRouter()


@router.get(
    path="/{user_id:uuid}",
    response_model=UserResponse,
    summary="Get user details",
    description="Retrieves details of a single user.",
    response_description="Details of a single user."
)
def get_user(request: Request, user_id: UUID4) -> UserResponse:
    user = UserService(
        db=request.state.db,
    ).get_user(user_id=str(user_id))

    request.state.audit(event=event.GET_USER)
    return user
