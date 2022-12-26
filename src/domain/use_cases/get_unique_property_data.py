from typing import Sequence


class GetUniquePropertyDataInteractor:

    def __init__(self, repository):
        self._repository = repository

    def execute(self, key) -> Sequence[tuple]:
        data = self._repository.get()
        if hasattr(data[0], key):
            result = set(map(lambda x: (getattr(x, key + '_id'), getattr(x, key)), self._repository.get()))
            return list(result)
        else:
            raise AttributeError(f'Object {type(data[0])} have not attribute {key}')
