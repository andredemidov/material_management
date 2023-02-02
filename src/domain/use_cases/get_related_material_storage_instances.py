from typing import List, Dict
from domain.entities import MaterialRequirement, MaterialStorage


class GetRelatedMaterialStorageInstances:

    def __init__(self, requirement_repository, material_storage_repository):
        self._requirement_repository = requirement_repository
        self._material_storage_repository = material_storage_repository

    @staticmethod
    def _find_storage_material(requirement: MaterialRequirement, storage_dict: Dict[str, Dict[str, MaterialStorage]]):
        onsite_storages_ids = requirement.onsite_storage_ids
        for related_material in requirement.related_materials:
            storages_by_code = storage_dict.get(related_material.code)
            if storages_by_code:
                for storage_id, storage in storages_by_code.items():
                    if storage_id in onsite_storages_ids:
                        related_material.onsite_storage.append(storage)
                    else:
                        related_material.remote_storage.append(storage)

    @staticmethod
    def _get_storage_dict(storages: List[MaterialStorage]) -> Dict[str, Dict[str, MaterialStorage]]:
        """возвращает словарь со структурой {'code' : {'storage_id': storage}}"""
        storage_dict = {}
        for storage in storages:
            if storage.code not in storage_dict:
                storage_dict[storage.code] = {}
            storage_dict[storage.code][storage.storage_id] = storage
        return storage_dict

    def execute(self):
        storages = self._material_storage_repository.get()
        storage_dict = self._get_storage_dict(storages)
        requirements_with_defined_storage = tuple(filter(lambda x: x.onsite_storage_ids, self._requirement_repository.get()))

        for requirement in requirements_with_defined_storage:
            self._find_storage_material(requirement, storage_dict)
        print('get storages instances complete')
