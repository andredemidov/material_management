from dataclasses import dataclass, field
from typing import List
from .material_supply import MaterialSupply
from .material_order import MaterialOrder
from .material_notification import MaterialNotification


@dataclass
class MaterialRelated:
    host: str
    code: str
    self_id: str = None
    item_id: str = None
    delete: bool = False
    supply: MaterialSupply = None
    free_supply: MaterialSupply = None
    order: MaterialOrder = None
    notification: MaterialNotification = None
    rest_supply: List[MaterialSupply] = field(default_factory=list)
    available: (int, float) = 0
    free_available: (int, float) = 0
    _rest_total_available: (int, float) = None
    rest_available: (int, float) = 0
    contractor_id: str = None
    moving: (int, float) = 0
    delivered: (int, float) = 0
    shipped_available: (int, float) = 0
    # текущие данные распределения поставки
    cur_available: (int, float) = 0
    cur_free_available: (int, float) = 0
    cur_rest_available: (int, float) = 0
    cur_moving: (int, float) = 0
    cur_delivered: (int, float) = 0
    cur_shipped_available: (int, float) = 0
    cur_rest_total_available: (int, float) = 0
    cur_issued: (int, float) = 0
    cur_supplied: (int, float) = 0
    cur_amount: (int, float) = 0
    cur_free_total_available: (int, float) = 0
    cur_total_moving: (int, float) = 0
    cur_total_shipped: (int, float) = 0
    cur_total_delivered: (int, float) = 0
    cur_name: str = ''

    def __str__(self):
        return self.code

    def __hash__(self):
        return hash(self.code)

    def __repr__(self):
        return self.code

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other
        elif isinstance(other, MaterialRelated):
            return self.code == other.code and self.host == other.host
        else:
            raise TypeError(f'Невозможно сравнить {type(self)} и {type(other)}')

    @property
    def rest_total_available(self):
        if self.rest_supply is not None:
            if self._rest_total_available is not None:
                return self._rest_total_available
            else:
                self._rest_total_available = sum(map(lambda x: x.available, self.rest_supply))
                return self._rest_total_available
        return 0

    @property
    def issued(self):
        if self.supply:
            return self.supply.issued
        else:
            return 0

    @property
    def supplied(self):
        if self.supply:
            return self.supply.supplied
        else:
            return 0

    @property
    def amount(self):
        if self.supply:
            return self.supply.amount
        else:
            return 0

    @property
    def free_total_available(self):
        if self.free_supply:
            return self.free_supply.amount
        else:
            return 0

    @property
    def total_moving(self):
        if self.order:
            return self.order.moving
        else:
            return 0

    @property
    def total_shipped(self):
        if self.notification:
            return self.notification.shipped
        else:
            return 0

    @property
    def total_delivered(self):
        if self.order:
            return self.order.delivered
        else:
            return 0

    @property
    def name(self):
        if self.supply:
            return self.supply.name
        elif self.free_supply:
            return self.free_supply.name
        elif self.rest_supply:
            return self.rest_supply[0].name
        else:
            return None

    def current_data_to_dict(self) -> dict:
        return {
            'supply_amount': round(self.cur_amount, 4),
            'issued': round(self.cur_issued, 4),
            'supplied': round(self.cur_supplied, 4),
            'moving': round(self.cur_moving, 4),
            'total_moving': round(self.cur_total_moving, 4),
            'total_delivered': round(self.cur_total_delivered, 4),
            'delivered': round(self.cur_delivered, 4),
            'shipped_available': round(self.cur_shipped_available, 4),
            'shipped_total_available': round(self.cur_total_shipped, 4),
            'available': round(self.cur_available, 4),
            'rest_total_available': round(self.cur_rest_total_available, 4),
            'rest_available': round(self.cur_rest_available, 4),
            'free_available': round(self.cur_free_available, 4),
            'free_total_available': round(self.cur_free_total_available, 4),
            'name': self.name,
        }

    def new_data_to_dict(self) -> dict:
        return {
            'supply_amount': round(self.amount, 4),
            'issued': round(self.issued, 4),
            'supplied': round(self.supplied, 4),
            'moving': round(self.moving, 4),
            'total_moving': round(self.total_moving, 4),
            'total_delivered': round(self.total_delivered, 4),
            'delivered': round(self.delivered, 4),
            'shipped_available': round(self.shipped_available, 4),
            'shipped_total_available': round(self.total_shipped, 4),
            'available': round(self.available, 4),
            'rest_total_available': round(self.rest_total_available, 4),
            'rest_available': round(self.rest_available, 4),
            'free_available': round(self.free_available, 4),
            'free_total_available': round(self.free_total_available, 4),
            'name': self.name,
        }

    def have_change(self):
        return self.current_data_to_dict() != self.new_data_to_dict()
