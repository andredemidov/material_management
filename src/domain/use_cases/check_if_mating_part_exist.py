from domain import entities


class CheckIfMatingPartExist:

    def __init__(self, requirements_repository):
        self._requirements_repository = requirements_repository

    @staticmethod
    def _get_key(requirement: entities.MaterialRequirement) -> str:
        key_attributes = [
            str(requirement.construction_object),
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

    @staticmethod
    def _get_total(requirement: entities.MaterialRequirement):
        amount = requirement.new_available + requirement.new_shipped_available + requirement.mounted
        if requirement.type == 'Труба':
            amount = amount / requirement.one_mass * 1000
        return amount

    def execute(self):
        diameter_filter = entities.Filter('diameter', 'exist', 'forvalidation')
        type_filter = entities.Filter('type', 'exist', 'forvalidation')
        requirements = self._requirements_repository.get(type_filter, diameter_filter)
        requirement_dict = self._get_dict(requirements)
        for requirement in requirements:
            amount = self._get_total(requirement)
            if requirement.type == 'Труба':
                # presence of more than 11 meters of tube means that it can be welded to itself
                if amount >= 11 and requirement.new_available + requirement.new_shipped_available > 0:
                    requirement.new_mating_part = True
                else:
                    key = self._get_key(requirement)
                    mating_parts = requirement_dict.get(key)
                    # mating_parts.remove(requirement)
                    # tubes = list(filter(lambda x: x.type == 'Труба', mating_parts))
                    # total_amount_tubes = sum([self._get_total(one) for one in tubes])
                    # if total_amount_tubes > 11 and requirement.new_available + requirement.new_shipped_available > 0:
                    #     requirement.new_mating_part = True

                    parts = list(filter(lambda x: x.type in ['Отвод', 'Тройник', 'Фланец', 'Переход', 'Заглушка'], mating_parts))
                    total_amount_parts = sum([self._get_total(one) for one in parts])
                    if total_amount_parts and requirement.new_available + requirement.new_shipped_available > 0:
                        requirement.new_mating_part = True
            elif requirement.type in ['Отвод', 'Тройник', 'Фланец', 'Переход', 'Заглушка']:
                key = self._get_key(requirement)
                mating_parts = requirement_dict.get(key)
                tubes = list(filter(lambda x: x.type == 'Труба', mating_parts))
                total_amount_tubes = sum([self._get_total(one) for one in tubes])
                if total_amount_tubes and requirement.new_available + requirement.new_shipped_available > 0:
                    requirement.new_mating_part = True
