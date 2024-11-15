import os
import io
import json
import yaml
import logging
import copy
from collections.abc import Mapping
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class DataHandler(ABC):
    encoding = "utf-8"

    def __init__(self, encoding=None):
        if encoding is not None:
            self.encoding = encoding

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    @property
    @abstractmethod
    def extension(self) -> str:
        """
        Abstract method/property that forces the implementation of attribute,
        that should return the file name extension for specific file handler.
        """

    @abstractmethod
    def read_file(self, filename: str) -> dict:
        """
        Abstract method that forces the implementation of file reading for
        specific file format.
        :param filename: file path value.
        :return: dict of loaded file content.
        """

    @abstractmethod
    def read_string(self, data) -> dict:
        """
        Abstract method that forces the implementation of loading of data in
        specified format.
        :param data: string or bytes array of data to be loaded.
        :return: dict of loaded file content.
        """

    def read(self, filename: str) -> dict:
        """
        Reads the given file by calling the implementation of read_file
        abstractmethod from specific file handler.
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(
                f"Configuration file '{filename}' does not exist."
            )
        try:
            return self.read_file(filename)
        except Exception as e:
            raise TypeError(
                f"Failed to load file '{filename}' in format {self.extension}."
            ) from e

    def load(self, data: "str | bytes | dict") -> Mapping:
        """
        Reads the given data by calling the implementation of read_string
        abstractmethod from specific file handler.
        """
        try:
            if isinstance(data, bytes):
                data = data.decode(self.encoding).replace("'", '"')
            elif isinstance(data, Mapping):
                return copy.deepcopy(data)
            return self.read_string(data)
        except Exception as e:
            raise TypeError(
                f"Failed to load data in format '{self.extension}'."
            ) from e


class YAMLHandler(DataHandler):
    extension: str = "yaml"

    def read_file(self, filename: str) -> dict:
        with io.open(filename, "r", encoding=self.encoding) as f:
            return yaml.safe_load(f)

    def read_string(self, data: str) -> dict:
        return yaml.safe_load(data)


class JSONHandler(DataHandler):
    extension: str = "json"

    def read_file(self, filename: str) -> dict:
        with io.open(filename, "r", encoding=self.encoding) as f:
            return json.loads(f.read())

    def read_string(self, data: str) -> dict:
        return json.loads(data)


data_handlers = {
    cls.extension: cls for cls in DataHandler.__subclasses__()
}
