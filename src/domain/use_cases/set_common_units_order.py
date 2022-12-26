from .set_common_units_abstract import SetCommonUnitsAbstract


class SetCommonUnitsOrder(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.moving = instance.moving * i
        instance.delivered = instance.delivered * i
        instance.unit = new_unit
