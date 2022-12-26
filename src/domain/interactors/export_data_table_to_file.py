class ExportDataTableToFile:

    def __init__(self, repository, log_adapter):
        self._repository = repository
        self._log_adapter = log_adapter

    def execute(self, path):
        self._log_adapter.write_info(f'Export data to file called. Total {self._repository.total} Path {path}')
        statistic = self._repository.export_to_file(path)
        count_success = statistic["success"]
        count_error = statistic["error"]
        self._log_adapter.write_info(f'Success {count_success}, error {count_error}')
