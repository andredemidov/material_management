from dataclasses import dataclass
from datetime import datetime


@dataclass
class MaterialNotification:
    code: str
    shipped: (int, float)
    max_delivery_date: datetime
    max_shipping_date: datetime
    unit: str = None
    _available: (int, float) = None

    @property
    def shipped_available(self):
        if self._available is None:
            return self.shipped
        else:
            return self._available

    @shipped_available.setter
    def shipped_available(self, value):
        if isinstance(value, (int, float)):
            if value >= 0:
                self._available = value
            else:
                self._available = 0
        else:
            raise TypeError(f'Невозможно установить значение {value} в переменную available.')

    def __eq__(self, other):
        if isinstance(other, MaterialNotification):
            return self.code == other.code
        if isinstance(other, str):
            return self.code == other
        else:
            raise TypeError(f'Невозможно сравнить {type(self)} и {type(other)}')
