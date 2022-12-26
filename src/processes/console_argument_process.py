import sys
import logging
from domain.repositories import MainRootRepository

from .abstract_process import AbstractProcess
from .operate_main_root_process import OperateMainRootProcess


class ConsoleArgumentProcess(AbstractProcess):

    def _start_process(self):
        mode = sys.argv[1]
        logging.info(f'Mode {mode}')
        # инициация репозитория строек
        main_root_repository = MainRootRepository(get_data_adapter=self._get_data_adapter)
        # получение главных корней - обрабатываемых строек
        main_roots = main_root_repository.get()
        logging.info(f'Total main roots {len(main_roots)}')

        for main_root in main_roots:
            OperateMainRootProcess(
                main_root=main_root,
                mode=mode,
                get_data_adapter=self._get_data_adapter,
                post_data_adapter=self._post_data_adapter,
            ).execute()
