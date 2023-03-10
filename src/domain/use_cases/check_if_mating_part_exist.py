from domain import entities


class CheckIfMatingPartExist:

    def __init__(self, requirements_repository):
        self._requirements_repository = requirements_repository

    @staticmethod
    def _get_key(requirement: entities.MaterialRequirement) -> str:
        key_attributes = [
            str(requirement.construction_subobject),
            str(requirement.level_3),
            str(requirement.level_4),
            str(requirement.diameter),
        ]
        return ';'.join(key_attributes)

    def _get_dict(self, requirements: list[entities.MaterialRequirement]) -> dict:
        """
        возвращает словарь со структурой {key: list[MaterialRequirement]}
        """
        requirement_dict = {}
        for requirement in requirements:
            key = self._get_key(requirement)
            if requirement_dict.get(key):
                requirement_dict[key].append(requirement)
            else:
                requirement_dict[key] = [requirement]

        return requirement_dict

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
            provided = provided / requirement.one_mass * 1000
        return provided

    def execute(self):
        welded_types = ['Отвод', 'Тройник', 'Фланец', 'Переход', 'Заглушка']
        diameter_filter = entities.Filter('diameter', 'exist', 'forvalidation')
        type_filter = entities.Filter('type', 'exist', 'forvalidation')
        requirements = self._requirements_repository.get(type_filter, diameter_filter)
        requirement_dict = self._get_dict(requirements)
        for requirement in requirements:
            provided = self._get_provided(requirement)
            if requirement.type == 'Труба':
                # presence of more than 11 meters of tube means that it can be welded to itself
                if self._get_total(requirement) >= 11 and provided > 0:
                    requirement.new_mating_part = True
                else:
                    key = self._get_key(requirement)
                    mating_parts = requirement_dict.get(key)
                    # mating_parts.remove(requirement)
                    # tubes = list(filter(lambda x: x.type == 'Труба', mating_parts))
                    # total_amount_tubes = sum([self._get_total(one) for one in tubes])
                    # if total_amount_tubes > 11 and requirement.new_available + requirement.new_shipped_available > 0:
                    #     requirement.new_mating_part = True

                    parts = list(filter(lambda x: x.type in welded_types, mating_parts))
                    total_amount_parts = sum([self._get_total(one) for one in parts])
                    if total_amount_parts and provided > 0:
                        requirement.new_mating_part = True
            elif requirement.type in welded_types:
                key = self._get_key(requirement)
                mating_parts = requirement_dict.get(key)
                tubes = list(filter(lambda x: x.type == 'Труба', mating_parts))
                total_amount_tubes = sum([self._get_total(one) for one in tubes])
                if total_amount_tubes and provided > 0:
                    requirement.new_mating_part = True
