from typing import Sequence
from .repository import Repository
from domain.entities import Root


class ChildRootRepository(Repository):

    def __init__(self, get_data_adapter, main_roots: list[Root] = None, entries: list = None):
        super().__init__(entries=entries, get_data_adapter=get_data_adapter)
        self.main_roots = list()
        if main_roots:
            self.main_roots.extend(main_roots)

    def _get_from_data_source(self):
        for main_root in self.main_roots:
            roots = self._get_data_adapter.get_child_roots(main_root)
            self.add(roots)

    def get_by_main_root(self, main_root: Root):
        if main_root in self.main_roots:
            result = list(filter(lambda x: x.parent_root == main_root.root_id, self._entries))
        else:
            result = self._get_data_adapter.get_child_roots(main_root)
            self.add(result)
            self.main_roots.append(main_root)
        return result

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, Root), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, Root):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of Root may be added into roots repository')
