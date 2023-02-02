from dataclasses import dataclass


@dataclass
class MaterialStorage:
    code: str
    reserved: (int, float)
    storage_id: str
    name: str = None
    storage_name: str = None
    root_id: str = None
    root_name: str = None
    unit: str = None
    _available: (int, float) = None

    @property
    def storage_available(self):
        if self._available is None:
            return self.reserved
        else:
            return self._available

    @storage_available.setter
    def storage_available(self, value):
        if isinstance(value, (int, float)):
            self._available = value
        else:
            raise TypeError(f'Невозможно установить значение {value} в переменную storage_available.')

    def reset_available(self):
        self._available = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            code=data.get('code'),
            reserved=data.get('reserved'),
            storage_name=data.get('storage_name'),
            storage_id=data.get('storage_id'),
            root_id=data.get('root_id'),
            root_name=data.get('root_name'),
            name=data.get('name'),
            unit=data.get('unit'),
        )

    def to_dict(self) -> dict:
        return {
            'code': self.code,
            'reserved': self.reserved,
            'root_id': self.root_id,
            'root_name': self.root_name,
            'storage_id': self.storage_id,
            'storage_name': self.storage_name,
            'name': self.name,
            'unit': self.unit,
        }

    def __eq__(self, other):
        if isinstance(other, MaterialStorage):
            return self.code == other.code and self.storage_id == other.storage_id
        if isinstance(other, str):
            return self.code == other
        else:
            raise TypeError(f'Невозможно сравнить {type(self)} и {type(other)}')
