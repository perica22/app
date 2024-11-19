from copy import deepcopy

from app.utils.config import Config


class ConfigMock(Config):
    def __init__(self, *args, **kwargs):
        self._init_data = deepcopy(kwargs.get("data"))
        super().__init__(*args, **kwargs)

    def initialize_again(self):
        self.__init__(data=self._init_data, path=self.path)


class ConfigServiceMock:
    def __init__(self, *args, **kwargs):
        self._config = ConfigMock(*args, **kwargs)

    @property
    def config(self):
        return self._config

    def clean_up(self):
        self._config.initialize_again()


class AppServiceMock(ConfigServiceMock):
    def __init__(self):
        super().__init__()
