from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MaterialRequirement:
    item_id: str
    name: str
    main_code: str
    construction: str
    construction_object: str
    construction_subobject: str
    level_4: str
    level_3: str
    project_section: str
    axes: str
    priority: str
    amount: (int, float)
    weld: (int, float)
    plan_date: (int, float)
    mounted: (int, float)
    mounted_spool: (int, float)
    # текущие данные по распределению
    cur_supply_amount: (int, float) = 0
    cur_issued: (int, float) = 0
    cur_supplied: (int, float) = 0
    cur_moving: (int, float) = 0
    cur_total_moving: (int, float) = 0
    cur_total_delivered: (int, float) = 0
    cur_delivered: (int, float) = 0
    cur_shipped_available: (int, float) = 0
    cur_shipped_total_available: (int, float) = 0
    cur_available: (int, float) = 0
    cur_rest_total_available: (int, float) = 0
    cur_rest_available: (int, float) = 0
    cur_free_available: (int, float) = 0
    cur_free_total_available: (int, float) = 0
    cur_max_date: datetime = None
    cur_codes_string: str = None
    cur_supply_request: str = None
    # необязательные
    model_element_list: list = field(default_factory=list)
    type: str = None
    type_supply: str = None
    diameter: (int, float) = 0
    unit: str = None
    original_unit: str = None
    original_amount: (int, float) = 0
    original_mounted: (int, float) = 0
    original_mounted_spool: (int, float) = 0
    one_mass: (int, float) = 0
    contractor_id: str = None
    contractor: str = None
    cad: str = ''
    codes_set: set = field(default_factory=set)
    related_materials: list = field(default_factory=list)

    # для распределения
    new_supply_amount: (int, float) = 0
    new_issued: (int, float) = 0
    new_supplied: (int, float) = 0
    new_moving: (int, float) = 0
    new_total_moving: (int, float) = 0
    new_total_delivered: (int, float) = 0
    new_delivered: (int, float) = 0
    new_shipped_available: (int, float) = 0
    new_shipped_total_available: (int, float) = 0
    new_available: (int, float) = 0
    new_rest_total_available: (int, float) = 0
    new_rest_available: (int, float) = 0
    new_free_available: (int, float) = 0
    new_free_total_available: (int, float) = 0
    new_max_date: datetime = None

    def __eq__(self, other):
        raise TypeError(f'Невозможно сравнить {type(self)} и {type(other)}')

    def __post_init__(self):
        self.name = self.name.strip()
        self.priority = self.priority if self.priority else 'a'
        self.original_amount = self.amount
        self.original_mounted = self.mounted
        self.original_mounted_spool = self.mounted_spool
        self.original_unit = self.unit
        if self.type == "Труба":
            self.amount = self.amount * self.one_mass / 1000
            self.mounted = self.mounted * self.one_mass / 1000
            self.mounted_spool = self.mounted_spool * self.one_mass / 1000
            self.unit = 'т'

    def __str__(self):
        return self.name

    @property
    def new_codes_string(self):
        return ';'.join(sorted(list(map(lambda x: x.code, self.related_materials))))

    @property
    def new_supply_request(self):
        result = set()
        for related_material in filter(lambda x: x.supply, self.related_materials):
            result.update(related_material.supply.supply_request)
        if None in result:
            result.remove(None)
        result = ';'.join(sorted(list(result)))
        return result

    @property
    def remainder(self):
        value = self.amount - self.mounted_spool - self.new_moving
        return value if value > 0 else 0

    @property
    def remainder_from_mounted(self):
        value = min(self.mounted, self.amount) - self.mounted_spool - self.new_moving
        return value if value > 0 else 0

    @property
    def total_available(self):
        return self.new_available + self.new_free_available + self.new_rest_available + self.new_shipped_available

    @property
    def remainder_for_moving(self):
        # смонтированное в спул количество здесь отнимается, потому что спцлы собираются другим подрядчиком, 
        # а остаток к перемещению учитывает только материалы текущего подрядчика
        return self.amount - self.mounted_spool

    @property
    def remainder_for_moving_from_mounted(self):
        # смонтированное количество, которое подлежит распределению в первую очередь
        if self.mounted == 0:
            return 0
        else:
            return min(self.mounted, self.amount) - self.mounted_spool

    def current_data_to_dict(self) -> dict:
        return {
            'supply_amount': round(self.cur_supply_amount, 8),
            'issued': round(self.cur_issued, 8),
            'supplied': round(self.cur_supplied, 8),
            'moving': round(self.cur_moving, 8),
            'total_moving': round(self.cur_total_moving, 8),
            'total_delivered': round(self.cur_total_delivered, 8),
            'delivered': round(self.cur_delivered, 8),
            'shipped_available': round(self.cur_shipped_available, 8),
            'shipped_total_available': round(self.cur_shipped_total_available, 8),
            'available': round(self.cur_available, 8),
            'rest_total_available': round(self.cur_rest_total_available, 8),
            'rest_available': round(self.cur_rest_available, 8),
            'free_available': round(self.cur_free_available, 8),
            'free_total_available': round(self.cur_free_total_available, 8),
            'max_date': self.cur_max_date,
            'codes_string': self.cur_codes_string,
            'supply_request': self.cur_supply_request,
        }

    def new_data_to_dict(self) -> dict:
        return {
            'supply_amount': round(self.new_supply_amount, 8),
            'issued': round(self.new_issued, 8),
            'supplied': round(self.new_supplied, 8),
            'moving': round(self.new_moving, 8),
            'total_moving': round(self.new_total_moving, 8),
            'total_delivered': round(self.new_total_delivered, 8),
            'delivered': round(self.new_delivered, 8),
            'shipped_available': round(self.new_shipped_available, 8),
            'shipped_total_available': round(self.new_shipped_total_available, 8),
            'available': round(self.new_available, 8),
            'rest_total_available': round(self.new_rest_total_available, 8),
            'rest_available': round(self.new_rest_available, 8),
            'free_available': round(self.new_free_available, 8),
            'free_total_available': round(self.new_free_total_available, 8),
            'max_date': self.new_max_date,
            'codes_string': self.new_codes_string,
            'supply_request': self.new_supply_request,
        }

    def have_change(self):
        return self.current_data_to_dict() != self.new_data_to_dict()

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'name': self.name,
            'main_code': self.main_code,
            'construction': self.construction,
            'construction_object': self.construction_object,
            'construction_subobject': self.construction_subobject,
            'level_4': self.level_4,
            'level_3': self.level_3,
            'project_section': self.project_section,
            'axes': self.axes,
            'priority': self.priority,
            'amount': round(self.amount, 8),
            'original_amount': round(self.original_amount, 8),
            'weld': self.weld,
            'plan_date': self.plan_date.strftime('%d.%m.%Y') if self.plan_date else None,
            'mounted': round(self.mounted, 8),
            'original_mounted': round(self.original_mounted, 8),
            'mounted_spool': round(self.mounted_spool, 8),
            'original_mounted_spool': round(self.original_mounted_spool, 8),
            # текущие данные по распределению
            'supply_amount': round(self.cur_supply_amount, 8),
            'issued': round(self.cur_issued, 8),
            'supplied': round(self.cur_supplied, 8),
            'moving': round(self.cur_moving, 8),
            'total_moving': round(self.cur_total_moving, 8),
            'total_delivered': round(self.cur_total_delivered, 8),
            'delivered': round(self.cur_delivered, 8),
            'shipped_available': round(self.cur_shipped_available, 8),
            'shipped_total_available': round(self.cur_shipped_total_available, 8),
            'available': round(self.cur_available, 8),
            'rest_total_available': round(self.cur_rest_total_available, 8),
            'rest_available': round(self.cur_rest_available, 8),
            'free_available': round(self.cur_free_available, 8),
            'free_total_available': round(self.cur_free_total_available, 8),
            'max_date': self.cur_max_date.strftime('%d.%m.%Y') if self.cur_max_date else None,
            'codes_string': self.cur_codes_string,
            'supply_request': self.cur_supply_request,
            # необязательные
            'type': self.type,
            'type_supply': self.type_supply,
            'diameter': self.diameter,
            'unit': self.unit,
            'original_unit': self.original_unit,
            'one_mass': self.one_mass,
            'contractor_id': self.contractor_id,
            'contractor': self.contractor,
        }
