from typing import Sequence
from domain.entities import Filter


class FilterMaterialRequirementInteractor:

    def __init__(self, repository):
        self._repository = repository

    def _get_entities(self, filters: Sequence[Filter] = None) -> list:
        result = []
        result.extend(self._repository.get())
        if filters:
            for filter_item in filters:
                result = list(filter(lambda x: self._check_by_filter(x, filter_item), result))
        return result

    def _check_by_filter(self, item, filter_item: Filter):
        if hasattr(item, filter_item.key):
            operator = f'__{filter_item.operator}__'
            if isinstance(filter_item.value, Sequence) and not isinstance(filter_item.value, str):
                flag = any(map(lambda x: self._check_one_key(item, filter_item.key, operator, x), filter_item.value))
            else:
                flag = self._check_one_key(item, filter_item.key, operator, filter_item.value)
            return flag
        else:
            raise AttributeError(f'Attribute {filter_item.key} not exist in item')

    @staticmethod
    def _check_one_key(item, key, operator, value):
        return getattr(getattr(item, key), operator)(value)

    def list_of_dicts(self, filter_list: Sequence[Filter] = None) -> Sequence[dict]:
        entities = self._get_entities(filter_list)
        return list(map(lambda x: x.to_dict(), entities))
