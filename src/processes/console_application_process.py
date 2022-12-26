import logging

from domain.entities import Root

from .abstract_process import AbstractProcess
from .operate_main_root_process import OperateMainRootProcess


class ConsoleApplicationProcess(AbstractProcess):

    def _start_process(self):
        print('Выбор режима')
        print('распределение - 1')
        print('удаление - 2')
        print('нормализация - 3')
        mode_number = None
        while mode_number is None:
            s = input('Введите: ')
            if s.isdigit() and s in ['1', '2', '3']:
                mode_number = int(s)
            else:
                print('Не удалось распознать запрос')

        if mode_number == 3:
            mode = 'normalization'
        elif mode_number == 2:
            mode = 'deleting'
        elif mode_number == 1:
            mode = 'distribution'
        else:
            mode = 'not determine'

        logging.info(f'Mode {mode}')

        print(mode)
        print('Указание идентификатора стройки для обработки')
        main_root_id = input('Указание id: ')
        print('Указание идентификатора титула для обработки')
        print('Возможно указание только одного титула, если нужно обработать все, то ничего не вводите')
        child_root_id = input('Указание титула: ')

        main_root = Root('main root', main_root_id)
        if child_root_id:
            child_root = Root('child root', child_root_id, main_root_id)
        else:
            child_root = None

        OperateMainRootProcess(
            main_root=main_root,
            mode=mode,
            get_data_adapter=self._get_data_adapter,
            post_data_adapter=self._post_data_adapter,
            child_root=child_root
        ).execute()

        input('Для завершения нажмите Ввод')
