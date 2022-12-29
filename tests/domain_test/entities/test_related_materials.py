import unittest
from random import choice
from src.domain.entities import MaterialRelated


class TestMaterialRelated(unittest.TestCase):

    @staticmethod
    def _get_fake_related_material() -> MaterialRelated:
        fake_related_material = MaterialRelated(
            host='forvalidation',
            code=choice(['0123456789', 'any_string', '', ' ', '0123', ' 0123456789']),
            validity_confirmed=choice([True, False]),
            name_valid=choice([True, False]),
            delete=choice([True, False]),
            self_id=choice(['id_exist', None])
        )
        return fake_related_material

    def test_code_valid_any_code_values_false_or_true(self):
        # arrange
        mock_related_materials = list(map(lambda x: self._get_fake_related_material(), range(500)))

        # assert
        for item in mock_related_materials:
            if isinstance(item.code, str) and item.code.isdigit() and len(item.code) == 10:
                self.assertEqual(item.code_valid, True)
            else:
                self.assertEqual(item.code_valid, False)

    def test_valid_random_data_true_or_false(self):
        # arrange
        mock_related_materials = list(map(lambda x: self._get_fake_related_material(), range(500)))

        # act
        result = list(filter(lambda x: x.valid(), mock_related_materials))

        # assert
        delete_or_invalid_code = list(filter(lambda x: x.delete or not x.code_valid, result))
        invalid_name_not_confirmed = list(filter(lambda x: not x.validity_confirmed and not x.name_valid, result))
        self.assertGreater(len(result), 0)
        self.assertEqual(len(delete_or_invalid_code), 0)
        self.assertEqual(len(invalid_name_not_confirmed), 0)
