import faker
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from tests.testing import AppPrecondition, AppVerificator
from app.service.includer.query import UserQueryIncluderFactory

generator = faker.Factory.create()


def test_get_user_successfully(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test get user successfully.

    Test scenario:
    1. Mock user
    2. Create request
    3. Verify response
    """
    user = given.user.exists()

    resp = client.get(url=f"/api/users/{str(user.id)}")

    verify.http.ok(resp)
    resp_data = resp.json()
    verify.user.check_user_info(response_data=resp_data, mocked_data=user)
    # check if include values are not within response
    for include in UserQueryIncluderFactory.query_includer_map.keys():
        assert include not in resp_data


def test_get_user_not_found(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
):
    """
    Test get user that does not exist.

    Test scenario:
    1. Create request
    2. Verify response
    """
    resp = client.get(url=f"/api/users/{str(uuid4())}")
    verify.http.not_found(resp)


@pytest.mark.parametrize(
    "include", ["posts,comments", "posts,test", "comments"]
)
def test_get_user_with_includes(
    given: AppPrecondition,
    verify: AppVerificator,
    client: TestClient,
    include: str
):
    """
    Test get user successfully with include values.

    Test scenario:
    1. Mock user, posts and comments
    2. Create request with include query parameter
    3. Verify user response and each included property
    """
    user = given.user.exists()
    post1 = given.post.exists(user_id=user.id)
    post2 = given.post.exists(user_id=user.id)
    post3 = given.post.exists(user_id=user.id)

    comment1 = given.comment.exists(user_id=user.id, post_id=post1.id)
    comment2 = given.comment.exists(user_id=user.id, post_id=post2.id)
    comment3 = given.comment.exists(user_id=user.id, post_id=post3.id)

    resp = client.get(url=f"/api/users/{str(user.id)}?include={include}")

    verify.http.ok(resp)
    resp_data = resp.json()
    verify.user.check_user_info(
        response_data=resp_data,
        mocked_data=user
    )
    for incl in include.split(","):
        if incl == "posts":
            verify.post.check_posts_info(
                response_data=resp_data[incl],
                mocked_data=[post1, post2, post3]
            )
        if incl == "comments":
            verify.comment.check_comments_info(
                response_data=resp_data[incl],
                mocked_data=[comment1, comment2, comment3]
            )
