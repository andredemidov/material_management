from typing import List
from domain.entities import MaterialRelated, MaterialRequirement
from data_sources.adapters import neosintez, excel


class PostDataAdapterFacade:

    def __init__(self, session):
        self._session = session

    def save_requirement(self, items: List[MaterialRequirement]) -> dict:
        return neosintez.SaveRequirementAdapter(self._session).execute(items)

    def save_related_material(self, items: List[MaterialRelated], only_validation_info=False) -> dict:
        return neosintez.SaveRelatedMaterialAdapter(self._session).execute(items, only_validation_info)

    def delete_related_materials(self, items: List[MaterialRelated]) -> dict:
        return neosintez.DeleteRelatedMaterialAdapter(self._session).execute(items)

    def create_related_material(self, items: List[MaterialRelated]) -> dict:
        return neosintez.CreateRelatedMaterialAdapter(self._session).execute(items)

    @staticmethod
    def export_to_excel(items, path) -> dict:
        return excel.ExportDataTableToFileAdapter(path).execute(items)
