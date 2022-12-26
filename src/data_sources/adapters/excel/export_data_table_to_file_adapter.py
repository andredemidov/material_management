import os.path
import re
from openpyxl import Workbook


class ExportDataTableToFileAdapter:

    def __init__(self, path: str):
        self._path = path

    def execute(self, items: list) -> dict:
        result = {'success': 0, 'error': 0}
        match = re.search('(.*/)', self._path)
        if not match or not os.path.isdir(match.group(1)):
            result['error'] = len(items)
            return result

        data = list(map(lambda x: x.to_dict(), items))
        workbook = Workbook()
        sheet = workbook.active
        headers = list(data[0].keys())
        rows = list(map(lambda x: list(x.values()), data))
        sheet.append(headers)
        for row in rows:
            sheet.append(row)

        workbook.save(filename=self._path)
        result['success'] = len(items)
        return result
