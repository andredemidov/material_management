from datetime import datetime


class GetSupplyDataForRequirements:

    def __init__(self, requirement_repository):
        self._requirement_repository = requirement_repository

    @staticmethod
    def _get_sum_total_value(a, b):
        return a + b

    @staticmethod
    def _get_max_date_total_value(a, b):
        if a and b:
            value = max(a, b)
        elif not b:
            value = a
        else:
            value = b
        return value

    @classmethod
    def _set_total_one(cls, requirement, supply_object, set_total_attr, supply_object_total_attr, option='sum'):
        set_total_attr_value = getattr(requirement, set_total_attr)
        supply_object_total_value = getattr(supply_object, supply_object_total_attr)
        value_options = {
            'sum': cls._get_sum_total_value,
            'max_date': cls._get_max_date_total_value,
        }
        setattr(requirement, set_total_attr, value_options[option](set_total_attr_value, supply_object_total_value))

    @staticmethod
    def _distribute_one(
            requirement,
            related_material,
            supply_object,
            supply_object_compare_attr,
            related_material_set_attr,
            compare_attr,
            set_attr,
            target_attr,
    ):
        supply_object_compare = getattr(supply_object, supply_object_compare_attr)
        target_value = getattr(requirement, target_attr)
        compare_value = getattr(requirement, compare_attr)
        set_value = getattr(requirement, set_attr)
        related_material_set_value = getattr(related_material, related_material_set_attr)

        if supply_object_compare > 0 and target_value < compare_value:
            if compare_value - target_value <= supply_object_compare:
                setattr(related_material, related_material_set_attr, compare_value - target_value)
                setattr(
                    supply_object,
                    supply_object_compare_attr,
                    supply_object_compare - (compare_value - target_value)
                )
                setattr(requirement, set_attr, set_value + compare_value - target_value)
            elif compare_value - target_value > supply_object_compare:
                setattr(related_material, related_material_set_attr, related_material_set_value + supply_object_compare)
                setattr(requirement, set_attr, set_value + supply_object_compare)
                setattr(supply_object, supply_object_compare_attr, 0)

    @classmethod
    def _distribute(
            cls,
            requirement,
            supply_object_attr,
            supply_object_compare_attr,
            related_material_set_attr,
            compare_attr,
            set_attr,
            target_attr,
            set_total_flag=True,
            total_attributes=None,
    ):
        if total_attributes is None:
            total_attributes = list()
        for related_material in requirement.related_materials:
            supply_object = getattr(related_material, supply_object_attr)
            kwargs = {
                'requirement': requirement,
                'related_material': related_material,
                'supply_object_compare_attr': supply_object_compare_attr,
                'related_material_set_attr': related_material_set_attr,
                'compare_attr': compare_attr,
                'set_attr': set_attr,
                'target_attr': target_attr,
            }
            if supply_object is None:
                continue
            elif isinstance(supply_object, list):
                for one_object in supply_object:
                    kwargs['supply_object'] = one_object
                    cls._distribute_one(**kwargs)
                    if set_total_flag:
                        for total_attribute in total_attributes:
                            cls._set_total_one(requirement, one_object, **total_attribute)
            else:
                kwargs['supply_object'] = supply_object
                cls._distribute_one(**kwargs)
                if set_total_flag:
                    for total_attribute in total_attributes:
                        cls._set_total_one(requirement, supply_object, **total_attribute)

    def _get_orders_data_new(self, requirement, set_total_flag=True, compare_attr='remainder_for_moving'):
        total_attributes = [
            {
                'supply_object_total_attr': 'moving',
                'set_total_attr': 'new_total_moving',
            },
        ]
        self._distribute(
            requirement=requirement,
            supply_object_attr='order',
            supply_object_compare_attr='remainder_moving',
            related_material_set_attr='moving',
            compare_attr=compare_attr,
            set_attr='new_moving',
            target_attr='moving',
            set_total_flag=set_total_flag,
            total_attributes=total_attributes
        )
        total_attributes = [
            {
                'supply_object_total_attr': 'delivered',
                'set_total_attr': 'new_total_delivered',
            },
        ]
        self._distribute(
            requirement=requirement,
            supply_object_attr='order',
            supply_object_compare_attr='remainder_delivered',
            related_material_set_attr='delivered',
            compare_attr=compare_attr,
            set_attr='new_delivered',
            target_attr='delivered',
            set_total_flag=set_total_flag,
            total_attributes=total_attributes
        )

    def _get_root_supply_data_new(self, requirement, set_total_flag=True, compare_attr='remainder'):
        total_attributes = [
            {
                'supply_object_total_attr': 'amount',
                'set_total_attr': 'new_supply_amount',
            },
            {
                'supply_object_total_attr': 'supplied',
                'set_total_attr': 'new_supplied',
            },
            {
                'supply_object_total_attr': 'issued',
                'set_total_attr': 'new_issued',
            },
            {
                'supply_object_total_attr': 'max_date',
                'set_total_attr': 'new_max_date',
                'option': 'max_date',
            },
        ]

        self._distribute(
            requirement=requirement,
            supply_object_attr='supply',
            supply_object_compare_attr='available',
            related_material_set_attr='available',
            compare_attr=compare_attr,
            set_attr='new_available',
            target_attr='total_available',
            set_total_flag=set_total_flag,
            total_attributes=total_attributes
        )

    def _get_notification_data_new(self, requirement, set_total_flag=True, compare_attr='remainder'):
        total_attributes = [
            {
                'supply_object_total_attr': 'shipped',
                'set_total_attr': 'new_shipped_total_available',
            },
        ]
        self._distribute(
            requirement=requirement,
            supply_object_attr='notification',
            supply_object_compare_attr='shipped_available',
            related_material_set_attr='shipped_available',
            compare_attr=compare_attr,
            set_attr='new_shipped_available',
            target_attr='total_available',
            set_total_flag=set_total_flag,
            total_attributes=total_attributes
        )

    def _get_free_supply_data_new(self, requirement, set_total_flag=True, compare_attr='remainder'):
        total_attributes = [
            {
                'supply_object_total_attr': 'total_available',
                'set_total_attr': 'new_free_total_available',
            },
        ]
        self._distribute(
            requirement=requirement,
            supply_object_attr='free_supply',
            supply_object_compare_attr='available',
            related_material_set_attr='free_available',
            compare_attr=compare_attr,
            set_attr='new_new_free_available',
            target_attr='total_available',
            set_total_flag=set_total_flag,
            total_attributes=total_attributes
        )

    def _get_rest_supply_data_new(self, requirement, set_total_flag=True, compare_attr='remainder'):
        total_attributes = [
            {
                'supply_object_total_attr': 'total_available',
                'set_total_attr': 'new_rest_total_available',
            },
        ]
        self._distribute(
            requirement=requirement,
            supply_object_attr='rest_supply',
            supply_object_compare_attr='available',
            related_material_set_attr='rest_available',
            compare_attr=compare_attr,
            set_attr='new_rest_available',
            target_attr='total_available',
            set_total_flag=set_total_flag,
            total_attributes=total_attributes
        )

    def _get_supply_data(self, requirements):
        for requirement in requirements:
            self._get_orders_data_new(requirement)
            self._get_root_supply_data_new(requirement)
            self._get_notification_data_new(requirement)
            self._get_free_supply_data_new(requirement)
            self._get_rest_supply_data_new(requirement)

    def _get_supply_data_for_mounted(self, requirements):
        for requirement in requirements:
            self._get_orders_data_new(requirement, compare_attr='remainder_for_moving_from_mounted', set_total_flag=False)
            self._get_root_supply_data_new(requirement, compare_attr='remainder_from_mounted', set_total_flag=False)
            self._get_notification_data_new(requirement, compare_attr='remainder_from_mounted', set_total_flag=False)
            self._get_free_supply_data_new(requirement, compare_attr='remainder_from_mounted', set_total_flag=False)
            self._get_rest_supply_data_new(requirement, compare_attr='remainder_from_mounted', set_total_flag=False)

    @staticmethod
    def _get_sort_date(x):
        max_date = datetime.strptime('2099-1-1', '%Y-%m-%d')
        min_date = datetime.strptime('2000-1-1', '%Y-%m-%d')
        if x.plan_date:
            return x.plan_date
        elif x.amount == x.mounted:
            return min_date
        else:
            return max_date

    def execute(self):
        requirements = self._requirement_repository.get_customer_supplied_with_main_code()
        requirements.sort(key=lambda x: x.name)
        requirements.sort(key=lambda x: x.level_4)
        requirements.sort(key=lambda x: self._get_sort_date(x))
        requirements.sort(key=lambda x: x.priority)
        self._get_supply_data_for_mounted(requirements)
        self._get_supply_data(requirements)
        print('get supply data for requirements complete')
