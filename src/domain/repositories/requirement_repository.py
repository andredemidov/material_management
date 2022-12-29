from typing import Sequence
from .repository import Repository
from domain.entities import Root, MaterialRequirement, Filter


class RequirementRepository(Repository):

    def __init__(self, post_data_adapter, get_data_adapter, root: Root,  entries: list = None):
        super().__init__(post_data_adapter=post_data_adapter, entries=entries, get_data_adapter=get_data_adapter)
        self._root = root

    @property
    def root_id(self):
        return self._root.root_id

    def _get_from_data_source(self):
        requirements = self._get_data_adapter.get_requirements(self._root)
        self.add(requirements)

    def save(self, changed=True) -> dict:
        if changed:
            requirements_for_save = list(filter(lambda x: x.have_change(), self._entries))
        else:
            requirements_for_save = self._entries

        return self._post_data_adapter.save_requirement(requirements_for_save)

    def get_own_supplied_with_main_code(self):
        filter_items = [
            Filter('type_supply', 'eq', 'Заказчик'),
            Filter('main_code', 'exist', 'forvalidation')
        ]
        return self.get(*filter_items)

    def check_if_marked_for_delete_is_exist(self):
        return self._get_data_adapter.get_delete_status(self._root)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, MaterialRequirement), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, MaterialRequirement):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of MaterialRequirement may be added into requirements repository')

    def export_to_file(self, path: str) -> dict:
        requirements = self.get()
        return self._post_data_adapter.export_to_excel(requirements, path)
