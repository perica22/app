import inject
import logging

from starlette.middleware.base import BaseHTTPMiddleware

from sb.db.sqlalchemy_utils import DBConfigurationException, do_commit

logger = logging.getLogger(__name__)


class StarletteDBMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, only_success_commit=False):
        """"""
        self.only_success_commit = only_success_commit
        super().__init__(app=app)

    async def dispatch(self, request, call_next):
        """Process request and response"""
        try:
            request.state.db = inject.instance("async_db")
        except inject.InjectorException:
            logger.error("Using DBMiddleware without injected db constant.")
            raise DBConfigurationException(
                "No 'db' in inject. It should provide creator for sessions."
            )

        # Perform request
        response = await call_next(request)
        response_ok = 200 <= response.status_code <= 299
        if (not self.only_success_commit) or response_ok:
            do_commit(request.state.db)
        else:
            request.state.db.close()
        registry = inject.instance("async_db_registry")
        registry.remove()
        return response
