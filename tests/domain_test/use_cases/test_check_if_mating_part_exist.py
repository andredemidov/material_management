import unittest
from domain import use_cases, entities, repositories
import random


class TestCheckIfMatingPartExist(unittest.TestCase):

    def setUp(self):

        types = ['Отвод', 'Тройник', 'Фланец', 'Переход', 'Заглушка', 'Труба', 'Прочее']
        requirements = list()
        x = 800
        for i in range(x):
            requirement = entities.MaterialRequirement(
                item_id='forvalidation',
                name='forvalidation',
                main_code='forvalidation',
                construction_object='forvalidation',
                level_4=f'level_4_{random.choice(range(x//10))}',
                axes='forvalidation',
                priority='forvalidation',
                amount=random.choice([1, 12]),
                plan_date=0,
                mounted=random.choice([0, 1, 12]),
                mounted_spool=0,
                construction='forvalidation',
                construction_subobject='subobject',
                level_3='level_3',
                project_section='forvalidation',
                weld=0,
                type=random.choice(types),
                diameter=random.choice([20, 50, 100, None])
            )
            requirement.one_mass = random.choice([50, 0]) if requirement.type == 'Труба' else 0
            requirement.new_available = random.choice([0, 1, 12]) if requirement.mounted == 0 else 0
            if requirement.mounted == 0 and requirement.new_available == 0:
                requirement.new_shipped_available = random.choice([0, 1, 12])
            else:
                requirement.new_shipped_available = 0

            requirements.append(requirement)
        self.stub_repository = repositories.RequirementRepository(None, None, None, requirements)

    @classmethod
    def _get_total(cls, requirement: entities.MaterialRequirement):
        return requirement.original_mounted + cls._get_provided(requirement)

    @staticmethod
    def _get_provided(requirement: entities.MaterialRequirement):
        provided = sum(
            [
                requirement.new_available,
                requirement.new_shipped_available,
                requirement.new_moving,
            ]
        )
        if requirement.type == 'Труба':
            provided = provided / requirement.one_mass * 1000 if requirement.one_mass else 1
        return provided

    def test_execute(self):
        welded_types = ['Отвод', 'Тройник', 'Фланец', 'Переход', 'Заглушка']

        # act
        use_cases.CheckIfMatingPartExist(self.stub_repository).execute()

        # assert
        rest = self.stub_repository.get(entities.Filter('type', 'eq', 'Прочее'))
        self.assertFalse(any([x.new_mating_part for x in rest]))

        diameter_filter = entities.Filter('diameter', 'exist', 'forvalidation')
        type_filter = entities.Filter('type', 'exist', 'forvalidation')
        for one in self.stub_repository.get(diameter_filter, type_filter):
            filters = [
                entities.Filter('construction_subobject', 'eq', one.construction_subobject),
                entities.Filter('level_3', 'eq', one.level_3),
                entities.Filter('level_4', 'eq', one.level_4),
                entities.Filter('diameter', 'eq', one.diameter),
            ]
            same_assembly = self.stub_repository.get(*filters, diameter_filter, type_filter)
            if one.type == 'Труба':
                possible_mating_parts = list(filter(lambda x: x.type in welded_types, same_assembly))
                assembly_condition = any([self._get_total(part) > 0 for part in possible_mating_parts])
                if (assembly_condition or self._get_total(one) >= 11) and self._get_provided(one) > 0:
                    self.assertTrue(one.new_mating_part)
                else:
                    self.assertFalse(one.new_mating_part)
            if one.type in welded_types:
                possible_mating_parts = list(filter(lambda x: x.type == 'Труба', same_assembly))
                assembly_condition = any([self._get_total(part) > 0 for part in possible_mating_parts])
                if assembly_condition and self._get_provided(one) > 0:
                    self.assertTrue(one.new_mating_part)
                else:
                    self.assertFalse(one.new_mating_part)
