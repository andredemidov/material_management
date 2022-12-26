from typing import Sequence
from .repository import Repository
from domain.entities import Root


class MainRootRepository(Repository):

    def __init__(self, get_data_adapter, entries: list = None):
        super().__init__(entries=entries, get_data_adapter=get_data_adapter)

    def _get_from_data_source(self):
        orders = self._get_data_adapter.get_main_roots()
        self.add(orders)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, Root), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, Root):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of Root may be added into roots repository')
