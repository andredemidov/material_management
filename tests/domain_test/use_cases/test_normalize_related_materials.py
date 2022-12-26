import unittest
from src.domain.entities.material_requirement import MaterialRequirement
from src.domain.entities import MaterialRelated
from src.domain.use_cases.normalize_related_materials import NormalizeRelatedMaterials


class TestNormalizeRelatedMaterials(unittest.TestCase):

    def test_execute_unnormalized_data_normalized_return(self):
        # arrange
        unnormalized_data = list()
        for i in range(4):
            related_materials = [
                MaterialRelated(host='forvalidation', code=f'{i}_001'),
                MaterialRelated(host='forvalidation', code=f'{i}_002')
            ]
            requirement = MaterialRequirement(
                item_id='forvalidation',
                name='forvalidation',
                main_code='forvalidation',
                construction_object='forvalidation',
                level_4='forvalidation',
                axes='forvalidation',
                priority='forvalidation',
                amount=0,
                plan_date=0,
                mounted=0,
                mounted_spool=0,
                related_materials=related_materials,
            )
            unnormalized_data.append(requirement)
        unnormalized_data[0].related_materials.append(MaterialRelated(host='forvalidation', code=f'common_code'))
        unnormalized_data[1].related_materials.append(MaterialRelated(host='forvalidation', code=f'common_code'))

        stub_repository = FakeRepository()
        stub_repository.fake_list = unnormalized_data
        # act
        NormalizeRelatedMaterials(stub_repository).execute()
        # assert
        result_data = list(
            map(lambda x: ','.join(sorted(list(map(lambda y: y.code, x.related_materials)))), stub_repository.list()))
        with_common_code = list(filter(lambda x: 'common_code' in x, result_data))
        without_common_code = list(filter(lambda x: 'common_code' not in x, result_data))
        self.assertGreater(len(with_common_code), 1)
        self.assertGreaterEqual(len(without_common_code), 1)
        self.assertEqual(len(set(with_common_code)), 1)


class FakeRepository:

    def __init__(self):
        self.fake_list = []

    def list(self):
        return self.fake_list
