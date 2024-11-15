import logging
import logging.config
import time
from sys import platform

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
    if "disable_existing_loggers" in new:
        config["disable_existing_loggers"] = new["disable_existing_loggers"]
    # Merge nested keys
    if "formatters" in new:
        if "formatters" not in config:
            config["formatters"] = {}
        for formatter, data in new["formatters"].items():
            config["formatters"][formatter] = data
    if "handlers" in new:
        if "handlers" not in config:
            config["handlers"] = {}
        for handler, data in new["handlers"].items():
            config["handlers"][handler] = data
    if "loggers" in new:
        if "loggers" not in config:
            config["loggers"] = {}
        for logger, data in new["loggers"].items():
            config["loggers"][logger] = data
    if "root" in new:
        if "root" not in config:
            config["root"] = {}
        for item, data in new["root"].items():
            config["root"][item] = data
    if "syslog" in new:
        if "syslog" not in config:
            config["syslog"] = {}
        for item, data in new["syslog"].items():
            config["syslog"][item] = data
    return config


def configure_develop_logging(application, config=None):
    """
    Configure application logging for development. This includes setting up
    all logging to go to console. If :param config: is provided it is used
    by merging it on top of default config.
    :param application: name of the application
    :param config: additional configuration for logging
        It must include following configuration if syslog is used in config:
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
        production=False,
        basic_config=dict(DEBUG_CONFIG),
        override=config
    )


def configure_production_logging(application, config):
    """
    Configure application logging for production. This includes setting up
    all logging to go to syslog. If :param config: is provided it is used
    by merging it on top of default config.
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
        basic_config=dict(PRODUCTION_CONFIG),
        override=config
    )


def _configure_logging(application, production, basic_config, override=None):
    """Configure the logging for the current application.

    The function sets up sbg-default logging.

    Default for production is syslog for all outputs,
    while for development default is console.

    All additional configurations can be passed through override parameter.
    Override can be used to override anything that is not a dictionary,
    everything that is a dictionary is simply merged. E.g. if you pass "root"
    handlers make sure that you add "syslog" as one of the list elements,
    otherwise you will have removed "syslog" logging from configuration

    For formatters there are few available that can be used without defining
    them completely (defined in basic config):
    ```
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
            "format": "%(application_name):   "
                      "%(levelname)11s: %(message)s "
                      "[%(name)s:%(lineno)d]",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        },
        "syslog_audit": {
            "format": "(application_name)-audit:   %(message)s",
            "datefmt": "%Y.%m.%d %H:%M:%S"
        }
    ```

    For successful logging in production your application must provide
    in override:
    ```
        {
            "syslog":
                "host": "host",  # no default
                "port": 514      # default value (int)
        }
    ```

    :param override: dictionary with app specific config
    :param production: which environment we setting up for
    :param str application: Application name used to determine where the
        logging configuration file and logging directory are.
    """

    # Load default configuration and populate application fields

    template = basic_config["formatters"]["syslog"]["format"]
    basic_config["formatters"]["syslog"]["format"] = template.format(
        application.lower())
    template = basic_config["formatters"]["syslog_audit"]["format"]
    basic_config["formatters"]["syslog_audit"]["format"] = template.format(
        application.lower())

    # Merge override if exists
    if override is not None:
        config = _merge_log_configs(basic_config, override)
    else:
        config = basic_config

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
    logger.info("Configuring logging for %s completed.",
                "production" if production else "development")
