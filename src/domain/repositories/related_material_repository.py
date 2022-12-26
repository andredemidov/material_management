from typing import Sequence
from .repository import Repository
from domain.entities import Root, MaterialRelated


class RelatedMaterialRepository(Repository):

    def __init__(self, post_data_adapter, get_data_adapter, root: Root, entries: list = None):
        super().__init__(post_data_adapter=post_data_adapter, get_data_adapter=get_data_adapter, entries=entries)
        self._root = root

    @property
    def root_id(self):
        return self._root.root_id

    def _get_from_data_source(self):
        related_materials = self._get_data_adapter.get_related_materials(self._root)
        self.add(related_materials)

    def save(self, changed=True):
        if changed:
            related_materials_for_save = list(filter(lambda x: x.have_change(), self._entries))
        else:
            related_materials_for_save = self._entries

        return self._post_data_adapter.save_related_material(related_materials_for_save)

    def delete_marked_for_delete(self):
        marked_for_delete = list(filter(lambda x: x.delete, self.get()))
        return self._post_data_adapter.delete_related_materials(marked_for_delete)

    def add(self, entries):
        if isinstance(entries, Sequence) and all(map(lambda x: isinstance(x, MaterialRelated), entries)):
            self._entries.extend(entries)
        elif isinstance(entries, MaterialRelated):
            self._entries.append(entries)
        else:
            raise TypeError('Only instance of MaterialRelated may be added into related materials repository')

    def create(self):
        related_materials_for_create = list(filter(lambda x: not x.delete and not x.self_id, self.get()))
        return self._post_data_adapter.create_related_material(related_materials_for_create)
