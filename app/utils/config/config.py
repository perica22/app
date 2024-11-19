import os
import logging
from collections.abc import Mapping, Iterator

from app.utils.config.data_handler import (
    JSONHandler, YAMLHandler, data_handlers
)

logger = logging.getLogger(__name__)
FILE_PATH = "/data/config/{}/{}"


class Path:
    """
    Class responsible for providing configuration files path.
    :param service_name: name of a service.
    :param fmt: string representing extension value for given file format.
    :param project_dir: current project path.
    """
    def __init__(self, service_name: str, fmt: str, project_dir: str) -> None:
        self.service_name = service_name
        self.fmt = fmt
        self.project_dir = project_dir

    def _get_file_path(self, filename: str) -> str:
        """
        Generates the path to desired configuration file.
        :param filename: name of the configuration file with extension.
        :return: path to the desired configuration file.
        """
        file_path = FILE_PATH.format(self.service_name, filename)
        return (
            file_path if os.path.isfile(file_path)
            else os.path.join(self.project_dir, "config", filename)
        )

    @property
    def config(self) -> str:
        """
        Generates the project configuration file path.
        :return: path to project config file.
        """
        filename = f"{self.service_name}.{self.fmt}"
        return self._get_file_path(filename)


class Config(Mapping):
    """
    Configuration class.
    :param filename: config file path.
    :param data: string, bytes or dictionary object of configuration data.
    :param fmt: string representing format of a config file.
    :param encoding: the encoding type a given data has to be encoded to.
    be processed.
    :param path: Path class instance. Only available if object is instantiated
    through from_application method as it requires project directory path.
    """

    def __init__(
        self,
        filename: str = None,
        data: "str | bytes | dict" = None,
        fmt: str = JSONHandler.extension,
        encoding: str = None,
        path: Path = None
    ) -> None:
        if fmt not in data_handlers:
            raise ValueError(f"Unsupported configuration format: {fmt}.")

        self.filename = filename
        self.fmt = fmt
        self.path = path

        data_handler = data_handlers[self.fmt](encoding=encoding)
        if filename is not None:
            self._data = data_handler.read(self.filename)
        elif data is not None:
            self._data = data_handler.load(data)
        else:
            self._data = {}

    def __repr__(self) -> str:
        if self.filename:
            return f"<Config(filename='{self.filename}')>"
        return f"<Config(format='{self.fmt}')>"

    def __iter__(self) -> Iterator:
        return (key for key in self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, item):
        """
        Retrieves the requested item.
        Knows how to resolve chained attributes(eg `services.enigma.address`),
        by splitting the given item by `.` value and retrieving elements
        one by one until the final is reached.
        :param item: string value of item to be retrieved.
        :return: can return any object that might be saved in a dictionary.
        """
        current = self._data
        for part in item.split("."):
            if isinstance(current, dict):
                current = current[part]
            elif isinstance(current, list):
                try:
                    part = int(part, 10)
                    current = current[part]
                except Exception:
                    raise IndexError(item)
            else:
                raise KeyError(item)
        return current

    @classmethod
    def from_filename(cls, filename: str) -> "Config":
        """
        Creates an instance of a class using provided configuration file path.
        :param filename: config file path.
        :return: Instance of a class.
        """
        filename = os.path.abspath(filename)
        fmt = os.path.splitext(filename)[-1].lower()[1:]
        return cls(filename=filename, fmt=fmt)

    @classmethod
    def from_data(
        cls, data: "str | bytes | dict",
        fmt: str = None,
        encoding: str = None
    ) -> "Config":
        """
        Creates an instance of a class using provided configuration data.
        :param data: string, bytes or dictionary object of configuration data.
        :param fmt: string representing format of a config file.
        :param encoding: the encoding type a given data has to be encoded to.
        :return: Instance of a class.
        """
        if fmt is None:
            fmt = JSONHandler.extension
        config_data = dict(data=data, fmt=fmt)
        if encoding is not None:
            config_data.update(encoding=encoding)
        return cls(**config_data)

    @classmethod
    def from_application(
        cls, application: str, project_dir: str, fmt: str = None
    ) -> "Config":
        """
        Creates an instance of a class, by providing a path property to Config
        object, which knows how to produce path to needed configuration files.
        :param application: application name for which config is being created.
        :param project_dir: current project directory path.
        :param fmt: string representing format of a config file.
        :return: Instance of a class.
        """
        if fmt is None:
            fmt = YAMLHandler.extension
        path = Path(application, fmt, project_dir)
        filename = path.config
        return cls(fmt=fmt, filename=filename, path=path)
