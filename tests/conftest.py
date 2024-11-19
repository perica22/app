from asyncio import current_task

import inject
import pytest
import contextlib
from fastapi import FastAPI
from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from fastapi.testclient import TestClient
import testing.postgresql
from pytest import FixtureRequest

from app.db import Base
from app.utils.config import Config
from app.server import Server
from tests.testing import AppServiceMock, AppPrecondition, AppVerificator


def configure_env(
    db_: testing.postgresql.Postgresql,
    mocks: AppServiceMock,
    binder: inject.Binder,
) -> None:
    """
    Inject configuration for testing environment.

    Note that inject requires callable with only one argument, so partial
    function should be created from this function and
    `testing.postgres.Postgresql` instance should be provided as first
    argument.

    :param db_: Temporary database to use for binding.
    :param binder: Inject binder.
    """
    engine = create_engine(
        db_,
        encoding="utf-8",
        isolation_level="REPEATABLE READ",
        echo=True
    )
    binder.bind("db_engine", engine)
    # expire_on_commit=False is here because sqlalchemy does not leave
    # objects in memory when session closes and it simplifies things a lot
    # for creating test data if these objects are left untouched.
    session_factory = sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )
    async_session_class = scoped_session(
        session_factory=session_factory,
        scopefunc=current_task
    )
    session_class = scoped_session(session_factory)

    binder.bind("db_registry", async_session_class)
    binder.bind_to_provider("db", async_session_class)
    binder.bind("thread_db_registry", session_class)
    binder.bind_to_provider("thread_db", session_class)

    # bind server
    binder.bind_to_constructor(FastAPI, Server)
    # bind services
    binder.bind(Config, mocks.config)


def env_kill(db_: testing.postgresql.Postgresql) -> None:
    """
    Stops and deletes provided database temporary database.

    :param db_: Temporary database to stop.
    :type db_: testing.postgres.Postgresql
    :return:
    """
    try:
        db_.stop()
    except Exception as e:
        print(f"Error stopping postgres {str(e)}")
    inject.clear()


def drop_db(engine) -> None:
    meta = Base.metadata
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
        trans.commit()


@pytest.fixture(scope="session")
def mocks(request: FixtureRequest) -> AppServiceMock:
    """Creates and returns all service mock."""
    _mocks = AppServiceMock()
    request.addfinalizer(_mocks.clean_up)
    return _mocks


@pytest.fixture
def given(request: FixtureRequest, mocks: AppServiceMock) -> AppPrecondition:
    """Creates precondition configurator."""
    _given = AppPrecondition(AppServiceMock)
    request.addfinalizer(mocks.clean_up)
    return _given


@pytest.fixture
def verify(mocks: AppServiceMock):
    """Returns instance of verificator."""
    return AppVerificator(mocks)


@pytest.fixture(scope="session")
def env(request, mocks) -> None:
    """Initializes temporary database for API tests."""

    mocks.config.initialize_again()
    postgres = testing.postgresql.Postgresql(
        initdb_args="-E=UTF-8 -U postgres -A trust"
    )
    request.addfinalizer(partial(env_kill, postgres))
    db_url = postgres.url()

    inject.clear_and_configure(partial(configure_env, db_url, mocks))


@pytest.fixture(scope="module")
def db_engine(env):
    """
    Returns database engine from environment.

    :param env:
        Dependency that environment should be set up for getting database
        engine.
    :return: Database engine.
    """
    yield inject.instance("db_engine")


@pytest.fixture
def init_schema(request, db_engine) -> None:
    """
    Creates database schema in provided database.

    :param request: Fixture request object.
    :param db_engine: Database reference where schema should be created.
    """
    Base.metadata.create_all(db_engine)
    request.addfinalizer(partial(drop_db, db_engine))


@pytest.fixture
def app(env):
    """
    Returns http server that should be tested.

    :param env: Dependency to environment configuration.
    """
    yield inject.instance(FastAPI).app


@pytest.fixture
def session():
    db_session = inject.instance("db")
    yield db_session
    db_session.rollback()
    db_session.close()


@pytest.fixture
def client(app: FastAPI):
    yield TestClient(app=app)


@pytest.fixture
def db(request, env):
    """
    Returns database from environment.

    :param env: Dependency that environment should be set up for getting
                database engine.
    :return: Database session
    :rtype: sqlalchemy.orm.Session
    """
    _db = inject.instance("db")
    yield _db
    _db.close()


# fixtures
@pytest.fixture(autouse=True)
def initialize(request, init_schema):
    """
    Dummy fixture used to force "init_data" to be applied to each function.
    """
    pass
