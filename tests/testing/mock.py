from copy import deepcopy

from app.utils.config import Config


class ConfigMock:

    def __init__(self, *args, **kwargs):
        self._config = Config(
            data={
                'data_init_enabled': True,
                'debug': True
            },
            *args,
            **kwargs
        )
        self._config_copy = deepcopy(self._config)
        # TODO
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # self.config.path.data_init = f'{dir_path}/data_init.json'

    @property
    def config(self):
        return self._config

    def clean_up(self):
        """Restores any changes made to configuration during testing."""
        self._config = deepcopy(self._config_copy)


class AppServiceMock(ConfigMock):
    def __init__(self):
        super().__init__()
