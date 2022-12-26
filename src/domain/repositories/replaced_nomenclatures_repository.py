from typing import Sequence
from .repository import Repository
from domain.entities import ReplacedNomenclature


class ReplacedNomenclaturesRepository(Repository):

    def __init__(self, get_data_adapter, entries: list = None):
        super().__init__(get_data_adapter=get_data_adapter, entries=entries)

    def _get_from_data_source(self):
        replaced_nomenclatures = self._get_data_adapter.get_replaced_nomenclatures()
        self.add(replaced_nomenclatures)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, ReplacedNomenclature), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, ReplacedNomenclature):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of ReplacedNomenclature may be added into replaced nomenclatures repository')
