import faker
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.db.post import PostStatusType
from tests.testing import AppPrecondition, AppVerificator
from app.service.includer.query import PostQueryIncluderFactory

generator = faker.Factory.create()


def test_get_post_successfully(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test get post successfully.

    Test scenario:
    1. Mock user and post for mocked user
    2. Create request
    3. Verify response
    """
    user = given.user.exists()
    post = given.post.exists(user_id=user.id)

    resp = client.get(url=f"/api/posts/{str(post.id)}")

    verify.http.ok(resp)
    resp_data = resp.json()
    verify.post.check_post_info(response_data=resp_data, mocked_data=post)
    # check if include values are not within response
    for include in PostQueryIncluderFactory.query_includer_map.keys():
        assert include not in resp_data


def test_get_post_not_found(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test get post that does not exist.

    Test scenario:
    1. Create request
    2. Verify response
    """
    resp = client.get(url=f"/api/posts/{str(uuid4())}")
    verify.http.not_found(resp)


def test_list_posts_successfully(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test list posts successfully.

    Test scenario:
    1. Mock user and posts for mocked user
    2. Create request
    3. Verify response
    """
    user = given.user.exists()
    post1 = given.post.exists(user_id=user.id)
    post2 = given.post.exists(user_id=user.id)
    post3 = given.post.exists(user_id=user.id)

    resp = client.get(url="/api/posts?include=user")

    verify.http.ok(resp)
    verify.post.check_posts_info(
        response_data=resp.json(), mocked_data=[post1, post2, post3]
    )


def test_list_posts_invalid_status_filter(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test list posts with invalid status filter.

    Test scenario:
    1. Create request with invalid status filter provided
    2. Verify response
    """
    resp = client.get(url="/api/posts?status=test")
    verify.http.validation_error(resp)


def test_list_posts_with_status_filter(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test list posts with filter status provided.

    Test scenario:
    1. Mock user
    2. Mock posts for user with different status
    2. Create request
    3. Verify response
    """
    user = given.user.exists()
    post1 = given.post.exists(user_id=user.id, status=PostStatusType.ACTIVE)
    post2 = given.post.exists(user_id=user.id)
    post3 = given.post.exists(user_id=user.id)

    resp = client.get(url="/api/posts?status=draft")

    verify.http.ok(resp)
    resp_data = resp.json()
    # assert if correct number of objects is returned
    assert len(resp_data) == 2
    verify.post.check_posts_info(
        response_data=resp_data, mocked_data=[post1, post2, post3]
    )


@pytest.mark.parametrize(
    "include", ["user,comments,tags", "user", "comments"]
)
def test_get_post_with_includes(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
    include: str
):
    """
    Test get post successfully with includes.

    Test scenario:
    1. Mock user, tags, post for mocked user and comments
    2. Create request
    3. Verify response and each included property
    """
    user = given.user.exists()

    tag1 = given.tag.exists()
    tag2 = given.tag.exists()

    post = given.post.exists(user_id=user.id, tags=[tag1, tag2])

    comment1 = given.comment.exists(user_id=user.id, post_id=post.id)
    comment2 = given.comment.exists(user_id=user.id, post_id=post.id)
    comment3 = given.comment.exists(user_id=user.id, post_id=post.id)

    resp = client.get(url=f"/api/posts/{str(post.id)}?include={include}")

    verify.http.ok(resp)
    resp_data = resp.json()
    verify.post.check_post_info(response_data=resp_data, mocked_data=post)

    for incl in include.split(","):
        if incl == "comments":
            verify.comment.check_comments_info(
                response_data=resp_data[incl],
                mocked_data=[comment1, comment2, comment3]
            )
        if incl == "tags":
            verify.tag.check_tags_info(
                response_data=resp_data[incl],
                mocked_data=[tag1, tag2]
            )
        if incl == "user":
            verify.user.check_user_info(
                response_data=resp_data[incl],
                mocked_data=user
            )


@pytest.mark.parametrize(
    "include", ["user,comments,tags, test", "tests"]
)
def test_get_post_with_invalid_includes(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
    include: str
):
    """
    Test get post with invalid includes.

    Test scenario:
    1. Create request with invalid include values
    2. Verify response
    """
    resp = client.get(url=f"/api/posts?include={include}")
    verify.http.validation_error(resp)


def test_get_posts_with_includes_and_status(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient
):
    """
    Test get post successfully with includes and status query parameter.

    Test scenario:
    1. Mock user, post for mocked user and comments
    2. Create request
    3. Verify response and each included property
    """
    user = given.user.exists()
    post1 = given.post.exists(user_id=user.id)
    post2 = given.post.exists(user_id=user.id, status=PostStatusType.ACTIVE)

    given.comment.exists(user_id=user.id, post_id=post1.id)
    comment2 = given.comment.exists(user_id=user.id, post_id=post2.id)
    comment3 = given.comment.exists(user_id=user.id, post_id=post2.id)

    resp = client.get(
        url="/api/posts?include=comments,user&status=active"
    )

    verify.http.ok(resp)
    resp_data = resp.json()
    assert len(resp_data) == 1
    verify.post.check_post_info(
        response_data=resp_data[0], mocked_data=post2
    )
    verify.comment.check_comments_info(
        response_data=resp_data[0]["comments"],
        mocked_data=[comment2, comment3]
    )
    verify.user.check_user_info(
        response_data=resp_data[0]["user"],
        mocked_data=user
    )
