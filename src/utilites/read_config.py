import json
from pathlib import Path


class ReadConfig:

    def execute(self) -> dict:
        config = {'authentication_config': self._read_authentication_config(), 'config': self._read_config()}
        return config

    @staticmethod
    def _read_authentication_config():
        authentication_config_path = Path(__file__).resolve().parent.parent.parent / 'authentication_config.json'
        with open(authentication_config_path) as authentication_config_file:
            authentication_config = json.loads(authentication_config_file.read())
        return authentication_config

    @staticmethod
    def _read_config():
        config_path = Path(__file__).resolve().parent.parent.parent / 'config.json'
        with open(config_path) as config_file:
            config = json.loads(config_file.read())
        return config
