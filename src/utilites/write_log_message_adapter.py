import logging
from datetime import datetime
import os.path
from .read_config import ReadConfig


class WriteLogMessageAdapter:

    def __init__(self):
        config = ReadConfig().execute()
        directory = config['config']['logs']['directory']
        now = datetime.now().strftime("%Y-%m-%d")
        if not os.path.isdir(directory):
            os.mkdir(directory)
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO,
            handlers=[
                logging.FileHandler(f'{directory}/{now}_material_management.log', encoding='UTF-8'),
                logging.StreamHandler()
            ]
        )

    @staticmethod
    def write_info(message):
        logging.info(message)

    @staticmethod
    def write_debug(message):
        logging.debug(message)

    @staticmethod
    def write_exception(message):
        logging.exception(message)
