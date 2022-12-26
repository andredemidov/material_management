import json
import os.path
from datetime import datetime
import logging
from data_sources import GetDataAdapterFacade, PostDataAdapterFacade, GetConnectionAdapter, CloseConnectionAdapter


class AbstractProcess:

    def __init__(self):
        self._url = None
        self._config = None
        self._authentication_config = None
        self._connection = None
        self._connection_adapter = None
        self._get_data_adapter = None
        self._post_data_adapter = None
        self._codes_replacement_file_path = None

    def _init_logging(self):
        directory = self._config['logs']['directory']
        if not os.path.isdir(directory):
            os.mkdir(directory)
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(f'{directory}/{self._get_time()}_material_management.log', encoding='UTF-8'),
                logging.StreamHandler()
            ]
        )

    def _read_authentication_config(self):
        authentication_config_path = os.path.dirname(os.getcwd()) + r'\authentication_config.json'
        with open(authentication_config_path) as authentication_config_file:
            self._authentication_config = json.loads(authentication_config_file.read())

    def _read_config(self):
        config_path = os.path.dirname(os.getcwd()) + r'\config.json'
        with open(config_path) as config_file:
            self._config = json.loads(config_file.read())

    @staticmethod
    def _get_time():
        """Функция возвращает текущую дату и время в строке формата Y-m-d"""
        return f'{datetime.now().strftime("%Y-%m-%d")}'

    def _start_process(self):
        pass

    def _init_adapters(self):
        self._connection_adapter = GetConnectionAdapter(self._url)
        self._connection = self._connection_adapter.execute(self._authentication_config['neosintez'])
        self._get_data_adapter = GetDataAdapterFacade(self._connection, self._codes_replacement_file_path)
        self._post_data_adapter = PostDataAdapterFacade(self._connection)

    def execute(self):
        self._read_config()
        self._read_authentication_config()
        self._init_logging()
        logging.info('Start')
        self._url = self._config['data_sources']['url']
        self._codes_replacement_file_path = self._config['data_sources']['codes_replacement_file_path']
        self._init_adapters()

        try:
            self._start_process()
        finally:
            self._finish_process()

    def _finish_process(self):
        if self._connection:
            CloseConnectionAdapter(self._connection).execute()
        logging.info('Connection is closed')
