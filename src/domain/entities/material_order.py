from dataclasses import dataclass
from datetime import datetime


@dataclass
class MaterialOrder:
    code: str
    contractor_id: str
    moving: (int, float)
    delivered: (int, float)
    creation_date: datetime = None
    unit: str = None
    _remainder_moving: (int, float) = None
    _remainder_delivered: (int, float) = None

    @property
    def remainder_moving(self):
        if self._remainder_moving is None:
            if self.creation_date and (datetime.now() - self.creation_date).days > 30:
                self._remainder_moving = self.delivered
            else:
                self._remainder_moving = self.moving
        return self._remainder_moving

    @remainder_moving.setter
    def remainder_moving(self, value):
        if isinstance(value, (int, float)):
            self._remainder_moving = value
        else:
            raise TypeError(f'Невозможно установить значение {value} в переменную remainder_moving')

    @property
    def remainder_delivered(self):
        if self._remainder_delivered is None:
            return self.delivered
        else:
            return self._remainder_delivered

    @remainder_delivered.setter
    def remainder_delivered(self, value):
        if isinstance(value, (int, float)):
            self._remainder_delivered = value
        else:
            raise TypeError(f'Невозможно установить значение {value} в переменную remainder_moving')

    def __eq__(self, other):
        if isinstance(other, MaterialOrder):
            return self.code == other.code and self.contractor_id == other.contractor_id
        else:
            return other == self
