from domain.entities import Root, MaterialRequirement, MaterialRelated


class GetRelatedMaterialsInstances:

    def __init__(self, requirement_repository, related_material_repository, root: Root):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        self._root = root

    def _operate_by_dict(self, requirements: list, related_materials: list):
        dict_of_hosts = {}
        for related_material in related_materials:
            dict_value = dict_of_hosts.get(related_material.host)
            if dict_value:
                dict_value.append(related_material)
            else:
                dict_of_hosts[related_material.host] = [related_material, ]
        print('get dict of related materials complete')
        for requirement in requirements:
            item_list = dict_of_hosts.pop(requirement.item_id, None)
            if item_list:
                requirement.related_materials = item_list
                for item in item_list:
                    item.contractor_id = requirement.contractor_id
            self._check_existing_related_material_with_main_code(requirement)

    def _check_existing_related_material_with_main_code(self, requirement: MaterialRequirement):
        if requirement.main_code not in requirement.related_materials:
            new_material_related = MaterialRelated(requirement.item_id, requirement.main_code)
            requirement.related_materials.append(new_material_related)
            self._related_material_repository.add(new_material_related)

    def execute(self):
        requirements = self._requirement_repository.get_own_supplied_with_main_code()
        requirements.sort(key=lambda x: x.item_id)
        related_materials = self._related_material_repository.get()
        related_materials.sort(key=lambda x: x.host)
        print('sort related materials complete. Start getting instances for requirements')
        self._operate_by_dict(requirements, related_materials)
        print('get related material instances complete')
