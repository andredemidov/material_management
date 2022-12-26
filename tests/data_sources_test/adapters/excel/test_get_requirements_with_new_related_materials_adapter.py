import unittest
from src.data_sources.adapters.excel.get_replaced_nomenclatures_adapter import GetReplacedNomenclatureAdapter


class TestGetReplacedNomenclatureAdapter(unittest.TestCase):

    def test_execute_file_not_exist_return_empty_list(self):
        # arrange
        file_path = ''
        # act
        result = GetReplacedNomenclatureAdapter(file_path).execute()
        # assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_execute_sample_input_sample_output(self):
        # arrange
        fake_data_from_excel = [
            {
                'Заменяемая код': '001',
                'Новая код': '002',
            },
            {
                'Заменяемая код': '001',
                'Новая код': '004',
            },
            {
                'Заменяемая код': '002',
                'Новая код': '001',
            },
            {
                'Заменяемая код': '003',
                'Новая код': '002',
            },
            {
                'Заменяемая код': '001',
                'Новая код': '003',
            },
        ]
        test_class = FakeGetReplacedNomenclature('')
        test_class.data_from_excel = fake_data_from_excel
        # act
        result = test_class.execute()

        # assert
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), len(fake_data_from_excel))

        results_has_attr_code = list(
            map(lambda x: all(list(map(lambda y: hasattr(y, 'code') and y.code, x.related_materials))), result))
        self.assertTrue(all(results_has_attr_code))

        result_unique_code_combinations = set(
            map(lambda x: ','.join(sorted(list(map(lambda y: y.code, x.related_materials)))), result))
        input_unique_code_combinations = set(map(lambda x: ','.join(sorted(list(x.values()))), fake_data_from_excel))
        self.assertEqual(result_unique_code_combinations, input_unique_code_combinations)


class FakeGetReplacedNomenclature(GetReplacedNomenclatureAdapter):

    def __init__(self, path):
        super().__init__(path)
        self.data_from_excel = None

    def _get_data_from_excel(self) -> list[dict]:
        return self.data_from_excel
