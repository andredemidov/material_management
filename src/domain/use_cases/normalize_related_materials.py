from domain.entities import MaterialRelated, MaterialRequirement


class NormalizeRelatedMaterials:

    def __init__(self, requirement_repository, related_material_repository, requirement_repository_source=None):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        if requirement_repository_source:
            self._repository_source = requirement_repository_source
        else:
            self._repository_source = requirement_repository

    @staticmethod
    def _get_valid_related_materials(requirement: MaterialRequirement):
        result = list(filter(lambda x: x.valid(), requirement.related_materials))
        return list(map(lambda x: x.code, result))

    def _get_unique_codes_sets(self):
        requirements = self._repository_source.get()
        unique_codes_sets = list(map(lambda req: set(self._get_valid_related_materials(req)), requirements))
        for i in range(len(unique_codes_sets)):
            j = i + 1
            while j < len(unique_codes_sets):
                if unique_codes_sets[i].intersection(unique_codes_sets[j]):
                    unique_codes_sets[i].update(unique_codes_sets[j])
                    del unique_codes_sets[j]
                else:
                    j += 1
        return unique_codes_sets

    def _normalize_related_materials(self, unique_codes_sets):
        """
        method adds related materials into requirement based on unique_codes_sets. Initially method updates attribute
        codes_set of requirement than initiates related_material for every code not existed in current
        related materials attribute
        """
        requirements = self._requirement_repository.get_own_supplied_with_main_code()
        for requirement in requirements:
            not_deleted_related_materials = list(filter(lambda x: x.valid(), requirement.related_materials))
            codes_set = set()
            for related_material in not_deleted_related_materials:
                rest_codes = list(filter(lambda x: related_material.code in x, unique_codes_sets))
                if not rest_codes:
                    continue
                codes_set.update(rest_codes[0])
            requirement.codes_set = codes_set
            for code in requirement.codes_set:
                if code not in requirement.related_materials:
                    related_material = MaterialRelated(host=requirement.item_id, code=code)
                    requirement.related_materials.append(related_material)
                    self._related_material_repository.add(related_material)

    def execute(self):
        unique_codes_sets = self._get_unique_codes_sets()
        self._normalize_related_materials(unique_codes_sets)
