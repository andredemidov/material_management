import logging

from domain.entities import Root
from domain.repositories import SupplyRepository, ChildRootRepository
from data_sources import GetDataAdapterFacade, PostDataAdapterFacade, GetConnectionAdapter, CloseConnectionAdapter
from utilites import ReadConfig, WriteLogMessageAdapter
from application.factories.operate_child_root_factory import OperateChildRootFactory


class ManageMainRoot:

    def __init__(self, factory=None):
        self._factory = factory if factory else OperateChildRootFactory()
        self._connection = None

    def execute(self, mode: str, main_root_id: str):
        WriteLogMessageAdapter()
        logging.info(f'manage main root {main_root_id} called. {mode}')
        config = ReadConfig().execute()
        url = config['config']['data_sources']['url']
        codes_replacement_file_path = config['config']['data_sources']['codes_replacement_file_path']
        try:
            connection_adapter = GetConnectionAdapter(url)
            self._connection = connection_adapter.execute(config['authentication_config']['neosintez'])
            get_data_adapter = GetDataAdapterFacade(self._connection, codes_replacement_file_path)
            post_data_adapter = PostDataAdapterFacade(self._connection)
            root = Root('forvalidation', main_root_id)
            child_root_repository = ChildRootRepository(
                get_data_adapter=get_data_adapter
            )

            main_supply_repository = SupplyRepository(
                get_data_adapter=get_data_adapter,
                main_root=root,
            )
            logging.info(f'getting all supply data')
            main_supply_repository.get()
            logging.info(f'supply data is got')
            kwargs = {
                'get_adapter': get_data_adapter,
                'post_adapter': post_data_adapter,
                'supply_repository': main_supply_repository,
            }
            tasks = []
            for child_root in child_root_repository.get_by_main_root(root):
                kwargs['child_root'] = child_root
                task = self._factory.create(mode, **kwargs)
                tasks.append(task)

            for task in tasks:
                try:
                    logging.info(task.info())
                    task.execute()
                    logging.info('completed')
                except Exception as e:
                    print(e)
                    logging.exception('Exception occurred while one task executing')

        except Exception as e:
            print(e)
            logging.exception('Exception occurred')
        finally:
            if self._connection:
                CloseConnectionAdapter(self._connection).execute()
                logging.info('Connection closed')
