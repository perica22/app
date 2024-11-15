from uvicorn_worker import UvicornWorker


class MultiplaWorker(UvicornWorker):  # type: ignore
    CONFIG_KWARGS = {
        **UvicornWorker.CONFIG_KWARGS,
        "access_log": False
    }
