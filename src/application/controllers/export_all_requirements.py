import logging
from domain.interactors import ExportDataTableToFile
from domain.repositories import RequirementRepository, MainRootRepository
from data_sources import GetDataAdapterFacade, PostDataAdapterFacade, GetConnectionAdapter, CloseConnectionAdapter
from utilites import ReadConfig, WriteLogMessageAdapter


class ExportAllRequirements:

    def __init__(self):
        self._connection = None

    def execute(self):
        log_adapter = WriteLogMessageAdapter()
        logging.info(f'Export all requirements to file')
        config = ReadConfig().execute()
        url = config['config']['data_sources']['url']
        requirements_data_export_file_path = config['config']['data_sources']['requirements_data_export_file_path']
        try:
            connection_adapter = GetConnectionAdapter(url)
            self._connection = connection_adapter.execute(config['authentication_config']['neosintez'])
            get_data_adapter = GetDataAdapterFacade(self._connection)
            post_data_adapter = PostDataAdapterFacade(self._connection)
            main_root_repository = MainRootRepository(
                get_data_adapter=get_data_adapter
            )
            all_requirements = list()
            for main_root in main_root_repository.get():
                requirements_repository = RequirementRepository(
                    post_data_adapter=post_data_adapter,
                    get_data_adapter=get_data_adapter,
                    root=main_root,
                )
                requirements = requirements_repository.get()
                all_requirements.extend(requirements)

            all_requirements_repository = RequirementRepository(
                    post_data_adapter=post_data_adapter,
                    get_data_adapter=get_data_adapter,
                    root=None,
                    entries=all_requirements
            )
            ExportDataTableToFile(all_requirements_repository, log_adapter).execute(requirements_data_export_file_path)

        except Exception as e:
            print(e)
            logging.exception('Exception occurred')

        finally:
            if self._connection:
                CloseConnectionAdapter(self._connection).execute()
                logging.info('Connection closed')
