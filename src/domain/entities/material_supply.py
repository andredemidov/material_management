from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MaterialSupply:
    code: str
    amount: (int, float)
    root_id: str
    root_name: str
    max_date: datetime
    issued: (int, float)
    supplied: (int, float)
    name: str
    unit: str = None
    supply_request: set = field(default_factory=set)
    _available: (int, float) = None

    @property
    def available(self):
        if self._available is None:
            return self.supplied - self.issued
        else:
            return self._available

    @available.setter
    def available(self, value):
        if isinstance(value, (int, float)):
            self._available = value
        else:
            raise TypeError(f'Невозможно установить значение {value} в переменную available.')

    def reset_available(self):
        self._available = None

    @property
    def total_available(self):
        return self.supplied - self.issued

    @classmethod
    def from_dict(cls, data: dict):
        instance = cls(
            code=data.get('code'),
            amount=data.get('amount'),
            root_id=data.get('root_id'),
            root_name=data.get('root_name'),
            max_date=datetime.strptime(data.get('max_date'), '%Y-%m-%d') if data.get('max_date') else None,
            issued=data.get('issued'),
            supplied=data.get('supplied'),
            name=data.get('name'),
            unit=data.get('unit'),
        )
        supply_request = data.get('supply_request')
        if supply_request:
            supply_request = set(supply_request.split(';'))
            instance.supply_request = supply_request
        return instance

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'amount': self.amount,
            'root_id': self.root_id,
            'root_name': self.root_name,
            'max_date': self.max_date.strftime('%Y-%m-%d') if self.max_date else None,
            'issued': self.issued,
            'supplied': self.supplied,
            'name': self.name,
            'unit': self.unit,
            'supply_request': ';'.join(sorted(list(self.supply_request))),
        }

    def __eq__(self, other):
        if isinstance(other, MaterialSupply):
            return self.code == other.code and self.root_id == other.root_id
        if isinstance(other, str):
            return self.code == other
        else:
            raise TypeError(f'Невозможно сравнить {type(self)} и {type(other)}')

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code
