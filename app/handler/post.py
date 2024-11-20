from pydantic import UUID4
from fastapi import APIRouter, Request

from app import event
from app.schema import PostResponse
from app.service import PostService
from app.filter import PostStatusFilter, IncludeFilter
from app.enum import PostIncludeFilter

router = APIRouter()


@router.get(
    path="",
    response_model=list[PostResponse],
    response_model_exclude_none=True,
    summary="List posts",
    description="Provides list of posts with their details.",
    response_description="List of objects with post details."
)
def list_posts(
    request: Request,
    status_filter: PostStatusFilter = PostStatusFilter.inject(),
    include_filter: IncludeFilter = IncludeFilter.inject(
        entity=PostIncludeFilter
    )
) -> list[PostResponse]:
    posts = PostService(
        db=request.state.db,
    ).list_posts(
        status=status_filter.value,
        include=include_filter.value
    )

    request.state.audit(event=event.LIST_POSTS)
    return posts


@router.get(
    path="/{post_id:uuid}",
    response_model=PostResponse,
    response_model_exclude_none=True,
    summary="Get single post",
    description="Get single post with with its details.",
    response_description="Single object containing post details."
)
def get_post(
    request: Request,
    post_id: UUID4,
    include_filter: IncludeFilter = IncludeFilter.inject(
        entity=PostIncludeFilter
    )
) -> PostResponse:
    post = PostService(
        db=request.state.db,
    ).get_post(
        post_id=str(post_id),
        include=include_filter.value
    )

    request.state.audit(event=event.GET_POST)
    return post
