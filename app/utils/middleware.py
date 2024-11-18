import inject
import logging
from typing import Optional

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.audit import AuditRecordCreator
from app.utils.db import do_commit
from app.event import Event

logger = logging.getLogger(__name__)


class DBMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        only_success_commit: Optional[bool] = False
    ) -> None:
        """"""
        self.only_success_commit = only_success_commit
        super().__init__(app=app)

    async def dispatch(self, request, call_next):
        """Process request and response"""
        try:
            request.state.db = inject.instance("db")
        except inject.InjectorException:
            logger.error("Using DBMiddleware without injected db constant.")
            raise Exception(
                "No 'db' in inject. It should provide creator for sessions."
            )

        # Perform request
        response = await call_next(request)
        response_ok = 200 <= response.status_code <= 299
        if (not self.only_success_commit) or response_ok:
            do_commit(session=request.state.db)
        else:
            request.state.db.close()
        registry = inject.instance("db_registry")
        registry.remove()
        return response


class AuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware that creates new audit record for each starlette request and
    attaches it to thread local. When request is finished it formats audit
    record and writes it to audit log file.
    """
    def __init__(self, app: FastAPI, application: str) -> None:
        """
        :param app: App object
        :param application: application name
        """
        self.application = application
        super().__init__(app=app)

    async def dispatch(self, request, call_next):
        """Process request and response"""

        # Process request
        request.state.audit = AuditRecordCreator(
            request, self.application
        )

        # Perform request
        response = await call_next(request)
        # Process response
        # Should not be logged if audit is not set (should not happen since
        # we set in in process_request) or if event on audit record is not
        # set (happens if nobody set event).
        if request.state.audit:
            # Checks if audit record creator class is set on request and there
            # is not events in its list and response status code is not OK.
            # That means that error has occurred during request handling and
            # special error event should be inserted in audit log.
            if (
                not request.state.audit.has_record
                and response.status_code >= 400
            ):
                request.state.audit(event=Event.from_error(
                    response=response,
                    request=request,
                ))

            request.state.audit.log_record(
                response_status=response.status_code
            )
        return response
