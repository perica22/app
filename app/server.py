from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.utils.middleware import StarletteDBMiddleware
from app.errors import generic_error_handler, http_error_handler
from app.version import __version__


class Server:
    def __init__(self):
        self.app = FastAPI(
            title="app",
            version=__version__,
            default_response_class=JSONResponse
        )
        attach_middlewares(app=self.app)
        attach_error_handlers(app=self.app)


def attach_middlewares(app: FastAPI):
    app.add_middleware(StarletteDBMiddleware, only_success_commit=True)


def attach_error_handlers(app: FastAPI):
    app.add_exception_handler(Exception, generic_error_handler)
    app.add_exception_handler(
        HTTPException, http_error_handler  # type: ignore
    )
    app.add_exception_handler(
        StarletteHTTPException, http_error_handler  # type: ignore
    )
