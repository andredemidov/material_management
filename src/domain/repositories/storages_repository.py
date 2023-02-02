from typing import Sequence
from .repository import Repository
from domain.entities import Root, MaterialStorage


class StoragesRepository(Repository):

    def __init__(self, get_data_adapter, root: Root, entries: list = None):
        super().__init__(entries=entries, get_data_adapter=get_data_adapter)
        self._root = root

    @property
    def root_id(self):
        return self._root.root_id

    def _get_from_data_source(self):
        storages = self._get_data_adapter.get_storages(self._root)
        self.add(storages)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, MaterialStorage), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, MaterialStorage):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of MaterialStorage may be added into storages repository')
