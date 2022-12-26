

class GetRelatedMaterialsForOneRequirement:

    def __init__(self, requirement_repository, adapter):
        self._requirement_repository = requirement_repository
        self._adapter = adapter

    def execute(self):
        requirements = self._requirement_repository.get_customer_supplied_with_main_code()

        for requirement in requirements:

            related_materials = self._adapter.get_related_materials(requirement)
            requirement.related_materials = related_materials
