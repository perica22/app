import faker
from uuid import uuid4

from fastapi.testclient import TestClient
from tests.testing import AppPrecondition, AppVerificator

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
    verify.user.check_user_info(response_data=resp.json(), mocked_user=user)


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
