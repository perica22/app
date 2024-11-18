import faker
from uuid import uuid4

from fastapi.testclient import TestClient

from app.db.post import PostStatusType
from tests.testing import AppPrecondition, AppVerificator

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
    verify.post.check_post_info(response_data=resp.json(), mocked_post=post)


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

    resp = client.get(url="/api/posts")

    verify.http.ok(resp)
    verify.post.check_posts_info(
        response_data=resp.json(), mocked_posts=[post1, post2, post3]
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
    verify.http.bad_request(resp)



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
    post1 = given.post.exists(user_id=user.id, status='ACTIVE')
    post2 = given.post.exists(user_id=user.id)
    post3 = given.post.exists(user_id=user.id)

    resp = client.get(url="/api/posts?status=draft")

    verify.http.ok(resp)
    resp_data = resp.json()
    # assert if correct number of objects is returned
    assert len(resp_data) == 2
    verify.post.check_posts_info(
        response_data=resp_data, mocked_posts=[post1, post2, post3]
    )
