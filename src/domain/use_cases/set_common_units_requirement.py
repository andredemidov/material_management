from domain.entities import MaterialRequirement
from .set_common_units_abstract import SetCommonUnitsAbstract


class SetCommonUnitsRequirement(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance: MaterialRequirement):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.mounted = instance.mounted * i
        instance.mounted_spool = instance.mounted_spool * i
        super()._calculate_and_set(instance)
