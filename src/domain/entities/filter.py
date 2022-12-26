from dataclasses import dataclass
from typing import Any, Sequence


@dataclass
class Filter:
    key: str
    operator: str
    value: Any

    def __post_init__(self):
        if self.operator not in ['eq', 'lt', 'gt', 'exist']:
            raise ValueError(f'Operator {self.operator} is not supported')

    def check(self, item) -> bool:
        if self.operator == 'exist':
            flag = bool(getattr(item, self.key))
        else:
            operator = f'__{self.operator}__'
            if isinstance(self.value, Sequence) and not isinstance(self.value, str):
                flag = any(map(lambda x: getattr(getattr(item, self.key), operator)(x), self.value))
            else:
                flag = getattr(getattr(item, self.key), operator)(self.value)
        return flag
