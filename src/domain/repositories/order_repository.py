from typing import Sequence
from .repository import Repository
from domain.entities import Root, MaterialOrder


class OrderRepository(Repository):

    def __init__(self, get_data_adapter, root: Root, entries: list = None):
        super().__init__(entries=entries, get_data_adapter=get_data_adapter)
        self._root = root

    @property
    def root_id(self):
        return self._root.root_id

    def _get_from_data_source(self):
        orders = self._get_data_adapter.get_orders(self._root)
        self.add(orders)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, MaterialOrder), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, MaterialOrder):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of MaterialOrder may be added into orders repository')
