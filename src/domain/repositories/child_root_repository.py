from typing import Sequence
from .repository import Repository
from domain.entities import Root, Filter


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
        if main_root not in self.main_roots:
            self.main_roots.append(main_root)
            self._get_from_data_source()

        result = self.get(Filter('parent_root', 'eq', main_root.root_id))
        return result

    def get_by_child_root_id(self, child_root_id: str) -> Root:
        filtered_roots = self.get(Filter('root_id', 'eq', child_root_id))
        if not filtered_roots:
            temp_root = Root('temp', child_root_id)
            # adapter has to returns a tuple (list[child_root], main_root)
            child_roots, main_root = self._get_data_adapter.get_child_roots_by_child_root(temp_root)
            if main_root and main_root not in self.main_roots:
                self.main_roots.append(main_root)
                self.add(child_roots)

            filtered_roots = self.get(Filter('root_id', 'eq', child_root_id))
        if filtered_roots:
            return filtered_roots[0]
        else:
            raise KeyError(f'There is no child root with id {child_root_id}')

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, Root), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, Root):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of Root may be added into roots repository')
