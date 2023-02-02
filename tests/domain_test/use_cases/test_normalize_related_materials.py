import unittest
from src.domain.entities.material_requirement import MaterialRequirement
from src.domain.entities import MaterialRelated
from src.domain.repositories import RequirementRepository, RelatedMaterialRepository
from src.domain.use_cases.normalize_related_materials import NormalizeRelatedMaterials


class TestNormalizeRelatedMaterials(unittest.TestCase):

    def setUp(self) -> None:
        unnormalized_data = list()
        for i in range(4):
            related_materials = [
                MaterialRelated(host='forvalidation', code=f'{i}123456789', name_valid=True),
                MaterialRelated(host='forvalidation', code=f'{i}989898989', name_valid=True),
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
                construction='forvalidation',
                construction_subobject='forvalidation',
                level_3='forvalidation',
                project_section='forvalidation',
                weld=0,
            )
            unnormalized_data.append(requirement)
        common_related_material = MaterialRelated(host='', code=f'0000000000', name_valid=True)
        common_related_material_delete = MaterialRelated(host='', code=f'0000000000', name_valid=True, delete=True)

        unnormalized_data[0].related_materials.append(common_related_material)
        unnormalized_data[1].related_materials.append(common_related_material)
        unnormalized_data[3].related_materials.append(common_related_material_delete)
        self.mock_with_delete_code = unnormalized_data[3]

        self.stub_repository = RequirementRepository(None, None, None, unnormalized_data)
        self.stub_repository_related_material = RelatedMaterialRepository(None, None, None)

    def test_execute_unnormalized_data_normalized_return(self):
        # arrange
        stub_repository = self.stub_repository
        stub_repository_related_material = self.stub_repository_related_material
        with_delete_common_code = self.mock_with_delete_code
        # act
        NormalizeRelatedMaterials(stub_repository, stub_repository_related_material).execute()
        # assert
        result_data = list(
            map(lambda x: ','.join(sorted(list(map(lambda y: y.code, x.related_materials)))), stub_repository.get()))
        with_common_code = list(filter(lambda x: '0000000000' in x, result_data))
        without_common_code = list(filter(lambda x: '0000000000' not in x, result_data))
        self.assertEqual(4, len(result_data))
        self.assertEqual(3, len(with_common_code))
        self.assertEqual(1, len(without_common_code))
        self.assertEqual(2, len(set(with_common_code)))
        self.assertEqual(3, len(with_delete_common_code.related_materials))

    def test_execute_invalid_item_not_distributed(self):
        # arrange
        stub_repository = self.stub_repository
        invalid_related_material = MaterialRelated(host='forvalidation', code='0001000111', name_valid=False)
        stub_repository.get()[0].related_materials.append(invalid_related_material)
        # act
        NormalizeRelatedMaterials(stub_repository, self.stub_repository_related_material).execute()
        # assert
        result_data = list(
            map(lambda x: ','.join(sorted(list(map(lambda y: y.code, x.related_materials)))), stub_repository.get()))
        with_invalid_name = list(filter(lambda x: '0001000111' in x, result_data))
        self.assertEqual(len(with_invalid_name), 1)

    def test_execute_validity_confirmed_name_valid_ignored(self):
        # arrange
        stub_repository = self.stub_repository
        checked_related_material = MaterialRelated(
            host='forvalidation',
            code=f'0001000111',
            name_valid=False,
            validity_confirmed=True
        )
        checked_related_material_with_invalid_code = MaterialRelated(
            host='forvalidation',
            code=f'invalid_code',
            name_valid=False,
            validity_confirmed=True
        )
        extended_related_material = [checked_related_material, checked_related_material_with_invalid_code]
        stub_repository.get()[0].related_materials.extend(extended_related_material)
        # act
        NormalizeRelatedMaterials(stub_repository, self.stub_repository_related_material).execute()
        # assert
        result_data = list(
            map(lambda x: ','.join(sorted(list(map(lambda y: y.code, x.related_materials)))), stub_repository.get()))
        with_checked_validity = list(filter(lambda x: '0001000111' in x, result_data))
        with_invalid_code = list(filter(lambda x: 'invalid_code' in x, result_data))
        self.assertGreater(len(with_checked_validity), 1)
        self.assertEqual(len(with_invalid_code), 1)
