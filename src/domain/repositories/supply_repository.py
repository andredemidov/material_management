from typing import Sequence
from copy import deepcopy
from domain.entities import MaterialSupply, Root
from .repository import Repository


class SupplyRepository(Repository):

    def __init__(self, get_data_adapter, child_root: Root = None, main_root: Root = None, entries: list = None):
        super().__init__(entries=entries, get_data_adapter=get_data_adapter)
        self._child_root = child_root
        self._main_root = main_root
        if not isinstance(child_root, Root) and not isinstance(main_root, Root):
            raise TypeError('both child root and main root was not determined')

    def _get_from_data_source(self):
        if self._main_root:
            supplies = self._get_data_adapter.get_supplies(self._main_root)
        else:
            supplies = self._get_data_adapter.get_supplies_by_child_root(self._child_root)
        self.add(supplies)

    @staticmethod
    def _check(supply: MaterialSupply, *root_id):
        return any(map(lambda x: supply.root_id == x, root_id))

    def get_by_root_id(self, root_id) -> list:
        supplies = self.get()
        return list(filter(lambda x: self._check(x, root_id), supplies))

    def get_excluding_root_id(self, *root_id) -> list:
        """Метод извлекает из репозитория экземпляры поставок кроме тех, которые относятся к указанному root_id.
        Принимает любое количество root_id в виде строки."""
        supplies = self.get()
        return list(filter(lambda x: not self._check(x, *root_id), supplies))

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, MaterialSupply), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, MaterialSupply):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of MaterialSupply may be added into supplies repository')

    def copy(self, return_initial=True):
        """Метод возвращает новый экземпляр репозитория с копией объектов вхождений. Флаг return_initial если True, то
        происходит откат данных по распределению внутри экземпляров поставок. По умолчанию True"""
        new_repository = SupplyRepository(
            get_data_adapter=self._get_data_adapter,
            child_root=self._child_root,
            main_root=self._main_root,
            entries=deepcopy(self._entries)
        )
        if return_initial:
            new_repository.return_initial_state()
        return new_repository

    def return_initial_state(self):
        for material_supply in self._entries:
            material_supply.reset_available()
