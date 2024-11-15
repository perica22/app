import sys
import inject
import logging

import uvicorn
from fastapi import FastAPI

from app.utils.config import Config

logger = logging.getLogger()


def main(args):
    from app import ioc
    inject.configure(ioc.production)

    logger.info(f"Started app with arguments: {', '.join(args)}")

    server = inject.instance(FastAPI)
    config = inject.instance(Config)
    uvicorn.run(
        app=server.app,
        host=config.get("server.host"),
        port=config.get("server.port")
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
