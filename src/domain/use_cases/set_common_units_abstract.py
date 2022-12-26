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
