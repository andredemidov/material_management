from typing import Collection
from domain.entities import MaterialSupply


class GetRelatedMaterialSupplyInstances:

    def __init__(self, requirement_repository, supply_repository):
        self._requirement_repository = requirement_repository
        self._supply_repository = supply_repository
        self._root_id = requirement_repository.root_id

    @staticmethod
    def _get_dict(supplies: Collection[MaterialSupply]) -> dict:
        result_dict = {}
        for item in supplies:
            dict_value = result_dict.get(item.code)
            if dict_value:
                dict_value.append(item)
            else:
                result_dict[item.code] = [item]
        return result_dict

    def execute(self):
        print('get supplies instances called')
        root_supplies_dict = self._get_dict(tuple(self._supply_repository.get_by_root_id(self._root_id)))
        rest_supplies_dict = self._get_dict(tuple(self._supply_repository.get_excluding_root_id(self._root_id, 'free')))
        free_supplies_dict = self._get_dict(tuple(self._supply_repository.get_by_root_id('free')))
        print('get supplies dict complete')

        for requirement in self._requirement_repository.get_own_supplied_with_main_code():

            for related_material in requirement.related_materials:
                # экземпляр поставки по текущему корню
                supply = root_supplies_dict.get(related_material.code)
                if supply:
                    related_material.supply = supply[0]

                # экземпляры поставки по другим корням
                related_material.rest_supply = rest_supplies_dict.get(related_material.code)

                # экземпляр поставки из свободных остатков
                free_supply = free_supplies_dict.get(related_material.code)
                if free_supply:
                    related_material.free_supply = free_supply[0]

        print('get supply instances complete')
