from pydantic import UUID4
from fastapi import APIRouter, Request

from app import event
from app.schema import PostResponse
from app.service import PostService

router = APIRouter()


@router.get(
    path="",
    response_model=list[PostResponse],
    summary="List posts",
    description="Provides list of posts with their details.",
    response_description="List of objects with post details."
)
def list_posts(request: Request) -> list[PostResponse]:
    posts = PostService(
        db=request.state.db,
    ).list_posts()

    request.state.audit(event=event.LIST_POSTS)
    return posts


@router.get(
    path="/{post_id:uuid}",
    response_model=PostResponse,
    summary="Get single post",
    description="Get single post with with its details.",
    response_description="Single object containing post details."
)
def get_post(request: Request, post_id: UUID4) -> PostResponse:
    post = PostService(
        db=request.state.db,
    ).get_post(post_id=str(post_id))

    request.state.audit(event=event.GET_POST)
    return post
