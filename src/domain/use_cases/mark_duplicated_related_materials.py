from domain.entities import MaterialRequirement


class MarkDuplicatedRelatedMaterials:

    def __init__(self, requirement_repository):
        self._requirement_repository = requirement_repository

    @staticmethod
    def _mark_duplicated_related_material(requirement: MaterialRequirement):
        for related_material in requirement.related_materials:
            if list(filter(lambda x: not x.delete, requirement.related_materials)).count(related_material) > 1:
                related_material.delete = True

    def execute(self):
        """Метод помечает на удаление дубликаты related_material во всех экземплярах requirement"""

        requirements = self._requirement_repository.get_customer_supplied_with_main_code()
        for requirement in requirements:
            self._mark_duplicated_related_material(requirement)
        print('mark duplicated materials complete')
