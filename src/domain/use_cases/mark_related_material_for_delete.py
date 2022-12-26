from typing import List
from domain.entities import MaterialRequirement


class MarkRelatedMaterialForDelete:

    def __init__(self, requirement_repository):
        self._requirement_repository = requirement_repository

    @staticmethod
    def _get_common_codes_for_delete(requirements_with_delete_codes: List[MaterialRequirement]) -> dict:
        """Метод выполняет итерацию по всем requirement в переданном списке и составляет dict с ключами
        requirement.main_code и значениями в виде set[str] с перечнем удаляемых кодов"""
        common_codes_for_delete = {}
        for req in requirements_with_delete_codes:
            delete_related_materials = set(filter(lambda c: c.delete, req.related_materials))
            delete_codes_str = set(map(lambda x: x.code, delete_related_materials))
            if req.main_code in common_codes_for_delete:
                common_codes_for_delete[req.main_code].update(delete_codes_str)
            else:
                common_codes_for_delete[req.main_code] = delete_codes_str
        return common_codes_for_delete

    @staticmethod
    def _mark_related_material(requirement: MaterialRequirement, common_codes_for_delete: dict):
        codes_for_delete = common_codes_for_delete.get(requirement.main_code, set())
        for related_material in filter(lambda x: x.code in codes_for_delete, requirement.related_materials):
            related_material.delete = True

    def execute(self):
        requirements = self._requirement_repository.get_customer_supplied_with_main_code()
        requirements_with_delete_codes = list(
            filter(lambda item: any(map(lambda c: c.delete, item.related_materials)), requirements)
        )
        common_codes_for_delete = self._get_common_codes_for_delete(requirements_with_delete_codes)

        for requirement in requirements:
            self._mark_related_material(requirement, common_codes_for_delete)
        print('mark related material for delete complete')
