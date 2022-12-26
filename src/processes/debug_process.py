import logging
import os.path
from domain.entities import Root

from .abstract_process import AbstractProcess
from .operate_main_root_process import OperateMainRootProcess


class DebugProcess(AbstractProcess):

    def _init_logging(self):
        log_path = os.path.dirname(os.getcwd()) + fr'\logs\{self._get_time()}.log'
        logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.DEBUG,
            handlers=[
                logging.FileHandler(log_path, encoding='UTF-8'),
                logging.StreamHandler()
            ]
        )

    def _read_config(self):
        self._config = {
            "data_sources": {
                "codes_replacement_file_path": "//irkoil/dfs/WorkDATA/OCOKS_IR_data/mt/code_replacement/izp_ozh.xlsx",
                "url": "https://construction.irkutskoil.ru/"
            },
            "logs": {
                "directory": "C:/python/logs"
            }
        }

    def _start_process(self):
        mode = 'distribution'
        main_root_id = '2ff70be7-1480-ec11-911c-005056b6948b'
        child_root_id = '59dc1740-151d-ed11-9140-005056b6948b'

        logging.info(f'Mode {mode}')

        main_root = Root(f'main root {main_root_id}', main_root_id)
        if child_root_id:
            child_root = Root(f'child root {child_root_id}', child_root_id, main_root_id)
        else:
            child_root = None

        OperateMainRootProcess(
            main_root=main_root,
            mode=mode,
            get_data_adapter=self._get_data_adapter,
            post_data_adapter=self._post_data_adapter,
            child_root=child_root
        ).execute()
