from domain.entities import Filter


class Repository:

    def __init__(self, post_data_adapter=None, get_data_adapter=None, entries: list = None):
        self._post_data_adapter = post_data_adapter
        self._get_data_adapter = get_data_adapter
        self._entries = []
        if entries:
            self._entries.extend(entries)

    @property
    def total(self):
        return len(self._entries)

    def get(self, *filters) -> list:
        """Возвращает копию списка вхождений. Принимает ряд аргументов filters в виде экземпляров Filter. Если передан
        один или несколько фильтров, то возвращает список с учетом фильтров."""
        if not self._entries:
            self._get_from_data_source()
        result = self._entries.copy()
        if filters:
            for filter_item in filters:
                result = list(filter(lambda x: self._check_by_filter(x, filter_item), result))
        return result

    @staticmethod
    def _check_by_filter(item, filter_item: Filter):
        if hasattr(item, filter_item.key):
            return filter_item.check(item)
        else:
            raise AttributeError(f'Attribute {filter_item.key} not exist in item')

    def _get_from_data_source(self):
        pass

    def add(self, entries: list):
        self._entries.extend(entries)
