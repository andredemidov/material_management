import logging
from domain.entities import Root
from domain.repositories import SupplyRepository, ChildRootRepository
from domain.use_cases import SetCommonUnitsSupply
from application.factories.operate_child_root_factory import OperateChildRootFactory


class OperateMainRootProcess:

    def __init__(
            self,
            main_root: Root,
            mode: str,
            get_data_adapter,
            post_data_adapter,
            child_root: Root = None
    ):
        self._main_root = main_root
        self._get_data_adapter = get_data_adapter
        self._post_data_adapter = post_data_adapter
        self._mode = mode
        self._child_root = child_root

    def _operate_child_root(self, root: Root, main_supply_repository):
        kwargs = {
            'child_root': root,
            'get_adapter': self._get_data_adapter,
            'post_adapter': self._post_data_adapter,
            'supply_repository': main_supply_repository,
        }
        factory = OperateChildRootFactory()
        process = factory.create(self._mode, **kwargs)
        logging.info(f'Processing {root.name}')

        try:
            process.execute()
            logging.info('Process complete')
        except Exception as e:
            print(e)
            logging.exception("Exception occurred")

    def execute(self):
        logging.info(f'Processing {self._main_root.name}')
        child_root_repository = ChildRootRepository(
            get_data_adapter=self._get_data_adapter
        )

        main_supply_repository = SupplyRepository(
            get_data_adapter=self._get_data_adapter,
            main_root=self._main_root,
            roots=child_root_repository.get_by_main_root(self._main_root)
        )

        if self._mode == 'distribution':
            main_supply_repository.get()
            SetCommonUnitsSupply(main_supply_repository).execute()

        # обработка объекта строительства в соответствии с конфигурацией
        if self._child_root:
            self._operate_child_root(self._child_root, main_supply_repository)
        else:
            logging.info(f'Total child roots {len(child_root_repository.get_by_main_root(self._main_root))}')

            for root in child_root_repository.get_by_main_root(self._main_root):
                self._operate_child_root(root, main_supply_repository)
