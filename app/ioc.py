import os
import logging
from asyncio import current_task

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

from app.utils.config import Config
from app.utils.db import make_connection_string
from app.utils.logging import (
    configure_develop_logging, configure_production_logging
)

from app.server import Server

logger = logging.getLogger(__name__)

PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def production(binder):
    binder.bind("PROJECT_DIR", PROJECT_DIR)
    # Bind configuration

    config = Config.from_application(
        application="multipla", project_dir=PROJECT_DIR
    )
    logger.info("Using config file: %s", config.path.config)
    binder.bind(Config, config)

    # Configure logging
    if config.get("debug", False):
        configure_develop_logging("app")
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    else:
        logging_conf = config.get("logging")
        configure_production_logging("app", logging_conf)

    # Bind database
    db_settings = config.get("database")
    connection = make_connection_string(config)
    connect_timeout = db_settings.get("connect_timeout", 5)
    pool_recycle = config.get("database.pool_recycle", 300)
    engine = create_engine(
        connection,
        encoding="utf-8",
        isolation_level="READ COMMITTED",
        poolclass=QueuePool,
        pool_recycle=pool_recycle,
        connect_args={"connect_timeout": connect_timeout},
    )
    session_factory = sessionmaker(bind=engine)
    async_session_class = scoped_session(
        session_factory, scopefunc=current_task
    )
    session_class = scoped_session(session_factory)

    binder.bind("db_registry", session_class)
    binder.bind_to_provider("db", session_class)
    binder.bind("db_engine", engine)
    binder.bind("async_db_registry", async_session_class)
    binder.bind_to_provider("async_db", async_session_class)

    # Bind server
    binder.bind_to_constructor(FastAPI, Server)

    # bind shell
    binder.bind("shell.namespace", {
        "config": config,
        "db": session_class(),
    })
