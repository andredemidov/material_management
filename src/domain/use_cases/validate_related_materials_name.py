import re


class ValidateRelatedMaterialsName:

    def __init__(self, requirements_repository):
        self._requirements_repository = requirements_repository

    def execute(self):
        requirements = self._requirements_repository.get()
        requirements = list(filter(lambda x: x.related_materials, requirements))
        pattern = '^(\S*)\s'
        for requirement in requirements:
            requirement_match = re.search(pattern, requirement.name)
            requirement_first_name = requirement_match.groups()[0] if requirement_match else None
            for related_material in requirement.related_materials:
                related_material_match = re.search(pattern, related_material.name)
                related_material_first_name = related_material_match.groups()[0] if related_material_match else None
                related_material.name_valid = requirement_first_name == related_material_first_name
