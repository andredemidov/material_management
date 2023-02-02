from domain.entities import MaterialRequirement, MaterialNotification, MaterialOrder, MaterialSupply, MaterialStorage


class SetCommonUnitsAbstract:

    UNITS = {
        'км': ('м', 1000),
    }

    def __init__(self, repository):
        self._repository = repository

    def _calculate_and_set(self, instance):
        new_unit, i = self.UNITS.get(instance.unit)
        instance.amount = instance.amount * i
        instance.unit = new_unit

    def execute(self):
        print('set common units called')
        instances = list(filter(lambda x: x.unit in self.UNITS, self._repository.get()))
        print('total instances for change unit', len(instances))
        for instance in instances:
            self._calculate_and_set(instance)


class SetCommonUnitsNotification(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance: MaterialNotification):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.shipped = instance.shipped * i
        instance.unit = new_unit


class SetCommonUnitsOrder(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance: MaterialOrder):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.moving = instance.moving * i
        instance.delivered = instance.delivered * i
        instance.unit = new_unit


class SetCommonUnitsRequirement(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance: MaterialRequirement):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.mounted = instance.mounted * i
        instance.mounted_spool = instance.mounted_spool * i
        super()._calculate_and_set(instance)


class SetCommonUnitsSupply(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance: MaterialSupply):

        new_unit, i = self.UNITS.get(instance.unit)
        instance.issued = instance.issued * i
        instance.supplied = instance.supplied * i
        super()._calculate_and_set(instance)


class SetCommonUnitsStorage(SetCommonUnitsAbstract):

    def _calculate_and_set(self, instance: MaterialStorage):
        new_unit, i = self.UNITS.get(instance.unit)
        instance.reserved = instance.reserved * i
        instance.unit = new_unit
