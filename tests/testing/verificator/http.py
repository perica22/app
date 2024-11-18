"""
Module for HTTP response code verification.
"""
from functools import partial as p

from fastapi import Response

from tests.testing import AppServiceMock
from tests.testing.verificator.base import Verificator


def _status_check(expected: int, resp: Response) -> None:
    """
    Verifies if provided status code matches provided http response and
    raises exception if it does not.

    :param expected: Desired status code.
    :param resp: Http response to check or its status code.
    """
    got = resp.status_code
    if got != expected:
        msg = f'Status code did not match, got {got}, expected {expected}'
        raise Exception(msg)


class HttpChecker:
    """
    Http response code validator.

    Just gather information to one place about http response codes and
    raises error if provided response code is not expected one.
    """
    # success
    ok = p(_status_check, 200)

    # client error
    bad_request = p(_status_check, 400)
    not_found = p(_status_check, 404)


class HttpVerificator(Verificator):
    """
    Http verificator class, which will be used for validating response status
    code
    """
    def __init__(self, mocks: AppServiceMock, **kwargs) -> None:
        """
        :param mocks: Service mocks.
        :type mocks: sb.http.testing.ServiceMock
        :return:
        """
        super().__init__(mocks=mocks)
        self.http = HttpChecker()
