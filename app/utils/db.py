import logging

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.utils.config import Config

logger = logging.getLogger(__name__)


def make_connection_string(config: Config) -> str:
    """
    :param config: Configuration object
    :return:
        Connection string suitable for usage in sqlalchemy based on values
        from provided configuration.
    """
    params = {"driver": "postgresql+psycopg2"}
    params.update(config.get("database"))
    if params.get("ssl", False):
        params["ssl"] = "?sslmode=require"
    else:
        params["ssl"] = ""
    conn_str_template = (
        "{driver}://{username}:{password}@{host}:{port}/{database}{ssl}"
    )

    return conn_str_template.format(**params)


def do_commit(session: Session) -> None:
    """
    Commits provided session and handles exceptions. Always closes session.
    """
    try:
        session.commit()
    except IntegrityError:
        logger.warning("Database integrity error on commit", exc_info=True)
        session.rollback()
        raise HTTPException(
            status_code=422,
            detail=(
                "Database integrity error - check if all data is provided "
                "and is in the right format."
            )
        )
        pass
    except Exception:
        logger.warning("Unable to commit DB transaction", exc_info=True)
        session.rollback()
        raise
    finally:
        session.close()
