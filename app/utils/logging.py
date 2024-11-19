import logging
import logging.config
import time
from sys import platform
from typing import Optional

logger = logging.getLogger(__name__)

PRODUCTION_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "syslog": {
        "connection_type": "port",
        "host": None,
        "port": 514
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s.%(msecs)03d   "
                      "%(levelname)11s: %(message)s [%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "simple": {
            "format": "%(levelname)-11s - %(message)s [%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "audit": {
            "format": "%(message)s"
        },
        "syslog": {
            "format": "{}:   %(levelname)11s: %(message)s "
                      "[%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "syslog_audit": {
            "format": "{}-audit:   %(message)s",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        }
    },
    "handlers": {
        "syslog": {
            "level": "INFO",
            "formatter": "syslog",
            "class": "logging.handlers.SysLogHandler",
            "address": None,
            "facility": "local1"
        },
        "syslog_audit": {
            "level": "INFO",
            "formatter": "syslog_audit",
            "class": "logging.handlers.SysLogHandler",
            "address": None,
            "facility": "local1"
        }
    },
    "loggers": {
        "audit": {
            "handlers": [
                "syslog_audit"
            ],
            "level": "INFO",
            "propagate": 0
        }
    },
    "root": {
        "handlers": [
            "syslog"
        ],
        "level": "INFO",
        "propagate": 1
    }
}

DEBUG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "sqlalchemy.engine": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s.%(msecs)03d   "
                      "%(levelname)11s: %(message)s "
                      "[%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "simple": {
            "format": "%(levelname)-11s - %(message)s [%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "audit": {
            "format": "%(message)s"
        },
        "syslog": {
            "format": "{}:   %(levelname)11s: %(message)s "
                      "[%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "syslog_audit": {
            "format": "{}-audit:   %(message)s",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "root": {
        "handlers": [
            "console"
        ],
        "level": "DEBUG",
        "propagate": 1
    }
}


class LoggerConnectionType:
    SOCKET = "socket"
    PORT = "port"


def _merge_log_configs(config, new):
    # Merge top level keys
    if "syslog" in new:
        if "syslog" not in config:
            config["syslog"] = {}
        for item, data in new["syslog"].items():
            config["syslog"][item] = data
    return config


def configure_develop_logging(application: str) -> None:
    """
    Configure application logging for development. This includes setting up
    all logging to go to console.
    :param application: name of the application
    """
    _configure_logging(
        application,
        production=False,
        config=DEBUG_CONFIG,
    )


def configure_production_logging(application: str, config: dict) -> None:
    """
    Configure application logging for production. This includes setting up
    all logging to go to syslog.
    :param application: name of the application
    :param config: additional configuration for logging
        It must include following configuration:
         ```
            "syslog":
                    {
                        "connection_type": "socket|port",
                        "host": "host for syslog address e.g. 127.0.0.1",
                        "port": "port for syslog address e.g. 514"
                    }
         ```
    """
    _configure_logging(
        application,
        production=True,
        config=PRODUCTION_CONFIG,
        override=config
    )


def _configure_logging(
    application: str,
    production: bool,
    config: dict,
    override: Optional[dict] = None
) -> None:
    """Configure the logging for the current application.

    For successful logging in production your application must provide
    in override:
    ```
        {
            "syslog":
                "host": "host",  # no default
                "port": 514      # default value (int)
        }
    ```

    :param production: which environment we setting up for
    :param str application: Application name used to determine where the
        logging configuration file and logging directory are.
    """

    # Load default configuration and populate application fields

    template = config["formatters"]["syslog"]["format"]
    config["formatters"]["syslog"]["format"] = template.format(
        application.lower())
    template = config["formatters"]["syslog_audit"]["format"]
    config["formatters"]["syslog_audit"]["format"] = template.format(
        application.lower())

    # Merge override if exists
    if override is not None:
        config = _merge_log_configs(config, override)
    else:
        config = config

    if production:
        # Define syslog connection
        if config["syslog"]["connection_type"] == LoggerConnectionType.PORT:
            syslog_address = (config["syslog"]["host"],
                              config["syslog"]["port"])
        else:
            if platform == "darwin":
                syslog_address = "/var/run/syslog"
            else:
                syslog_address = "/dev/log"

        config["handlers"]["syslog"]["address"] = syslog_address
        config["handlers"]["syslog_audit"]["address"] = syslog_address

    logging.Formatter.converter = time.gmtime
    # Configure logging
    logging.config.dictConfig(config)
    logger.info(
        "Configuring logging for "
        f"{'production' if production else 'development'} completed."
    )
