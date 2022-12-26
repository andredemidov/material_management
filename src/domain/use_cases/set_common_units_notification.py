from .set_common_units_abstract import SetCommonUnitsAbstract


class SetCommonUnitsNotification(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.shipped = instance.shipped * i
        instance.unit = new_unit
