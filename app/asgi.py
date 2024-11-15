"""Module for main app definition. This is the main ASGI module."""
import inject
import logging
from fastapi import FastAPI

from app.ioc import production

inject.configure(production)

logger = logging.getLogger(__name__)
logger.info("Starting app")

server = inject.instance(FastAPI)

app = server.app
