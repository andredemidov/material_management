import os.path
from typing import List
from openpyxl import load_workbook
from domain.entities import ReplacedNomenclature, MaterialRelated


class GetReplacedNomenclatureAdapter:

    def __init__(self, codes_replacement_file_path: str):
        self._codes_replacement_file_path = codes_replacement_file_path

    def _get_data_from_excel(self) -> list[dict]:
        if not os.path.isfile(self._codes_replacement_file_path):
            return []
        workbook = load_workbook(self._codes_replacement_file_path)
        sheet = workbook['TDSheet']
        headers = list(sheet.values)[0]
        data = list(sheet.values)[1:]
        data_dict = list(map(lambda x: dict(zip(headers, x)), data))
        return data_dict

    @staticmethod
    def _init_related_material(related_materials_codes: list[str]) -> List[MaterialRelated]:
        related_materials = list()
        for code in related_materials_codes:
            related_materials.append(MaterialRelated(host='forvalidation', code=code))
        return related_materials

    @staticmethod
    def _check_replaced_data(replaced_data: list[dict]):
        flag = False
        if replaced_data and isinstance(replaced_data, list) and isinstance(replaced_data[0], dict):
            keys = replaced_data[0].keys()
            if 'Заменяемая код' in keys and 'Новая код' in keys:
                flag = True
        return flag

    def _init_replaced_nomenclature(self, requirement_data) -> ReplacedNomenclature:
        related_materials_codes = [
            requirement_data['Заменяемая код'],
            requirement_data['Новая код'],
        ]
        related_materials = self._init_related_material(related_materials_codes)
        requirement = ReplacedNomenclature(related_materials=related_materials)
        return requirement

    def execute(self) -> List[ReplacedNomenclature]:
        replaced_nomenclatures = list()
        replaced_data = self._get_data_from_excel()
        if not self._check_replaced_data(replaced_data):
            return replaced_nomenclatures

        for one_data in replaced_data:
            replaced_nomenclatures.append(self._init_replaced_nomenclature(one_data))
        return replaced_nomenclatures
