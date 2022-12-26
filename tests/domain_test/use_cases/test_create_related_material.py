import unittest
from domain.use_cases.create_related_material import CreateRelatedMaterial
from domain.entities.material_requirement import MaterialRequirement
from domain.entities.material_related import MaterialRelated
from domain.repositories.repository import Repository


class TestCreateRelatedMaterial(unittest.TestCase):

    def test_create_related_material_sample_data_right_return(self):
        # arrange
        mock_adapter = FakeAdapter()
        stub_requirements = list()
        for i in range(10):
            stub_related_materials = [
                MaterialRelated(host='forvalidation', code='forvalidation', self_id=f'value{i}', delete=True),
                MaterialRelated(host='forvalidation', code='forvalidation', self_id=f'value{i}', delete=False),
                MaterialRelated(host='forvalidation', code='forvalidation', delete=False),
                MaterialRelated(host='forvalidation', code='forvalidation', delete=True),
            ]
            stub_requirement = MaterialRequirement(
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
                related_materials=stub_related_materials,
            )
            stub_requirements.append(stub_requirement)
        stub_repository = Repository(stub_requirements)
        # act
        result = CreateRelatedMaterial(stub_repository, mock_adapter).execute()
        # assert
        for_create = list()
        for stub_req in stub_requirements:
            for_create.append(list(filter(lambda x: not x.delete and not x.self_id, stub_req.related_materials)))
        expected_length = len(for_create)

        self.assertEqual(len(result), expected_length)
        self.assertEqual(len(list(filter(lambda x: x.delete, result))), 0)
        self.assertEqual(len(list(filter(lambda x: x.self_id, result))), 0)


class FakeAdapter:

    @staticmethod
    def create_related_material(related_materials_for_create):
        return related_materials_for_create
