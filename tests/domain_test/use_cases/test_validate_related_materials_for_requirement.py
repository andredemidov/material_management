import unittest
from domain.use_cases.validate_related_materials_name import ValidateRelatedMaterialsName
from domain.entities.material_related import MaterialRelated
from domain.entities.material_requirement import MaterialRequirement
from domain.repositories.requirement_repository import RequirementRepository


class TestValidateRelatedMaterialsForRequirement(unittest.TestCase):

    def test_execute_wrong_name_have_false_valid_name(self):
        # arrange
        names = [
            'Отвод 170х22 ГОСТ',
            'Отвод 140',
            'Тройник 140',
            'Лист 140',
        ]
        mock_related_materials = list(map(lambda x: MaterialRelated('forvalidation', 'forvalidation', x), names))
        stub_requirement = MaterialRequirement(
                item_id='forvalidation',
                name='Тройник 120х12х120 ГОСТ 111111',
                main_code='forvalidation',
                construction_object='forvalidation',
                level_4='forvalidation',
                axes='forvalidation',
                priority='forvalidation',
                amount=0,
                plan_date=0,
                mounted=0,
                mounted_spool=0,
                related_materials=mock_related_materials,
                construction='forvalidation',
                construction_subobject='forvalidation',
                level_3='forvalidation',
                project_section='forvalidation',
                weld=0,
            )
        stub_repository = RequirementRepository(None, None, None, [stub_requirement])

        # act
        ValidateRelatedMaterialsName(stub_repository).execute()

        # assert
        self.assertEqual(len(list(filter(lambda x: x.name_valid, mock_related_materials))), 1)
        self.assertEqual(len(list(filter(lambda x: x.name_valid is None, mock_related_materials))), 0)
