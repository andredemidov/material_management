from typing import List
from domain.entities import MaterialSupply, MaterialNotification, Root


class CalculateNotificationsAvailable:

    def __init__(self, material_notification_repository, supply_repository, root: Root):
        self._material_notification_repository = material_notification_repository
        self._supply_repository = supply_repository
        self._root = root

    @staticmethod
    def _calculate(supplies: List[MaterialSupply], notifications: List[MaterialNotification]):
        for material in notifications:
            index = supplies.index(material.code)
            supply = supplies.pop(index)
            material.shipped_available = material.shipped - supply.supplied

    def execute(self):
        supplies = self._supply_repository.get_by_root_id(self._root.root_id)
        supplies.sort(key=lambda x: x.code)
        notifications = self._material_notification_repository.get()
        notifications.sort(key=lambda x: x.code)
        supplies = list(filter(lambda x: x.code in notifications, supplies))
        notifications = list(filter(lambda x: x.passed_date and x.code in supplies, notifications))
        self._calculate(supplies, notifications)
