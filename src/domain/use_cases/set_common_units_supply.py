from .set_common_units_abstract import SetCommonUnitsAbstract


class SetCommonUnitsSupply(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.issued = instance.issued * i
        instance.new_supplied = instance.new_supplied * i
        super()._calculate_and_set(instance)
