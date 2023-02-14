from typing import List
from domain.entities import MaterialSupply, MaterialNotification, Root


class CalculateNotificationsAvailable:

    def __init__(self, material_notification_repository, supply_repository, root: Root):
        self._material_notification_repository = material_notification_repository
        self._supply_repository = supply_repository
        self._root = root

    @staticmethod
    def _calculate(supplies_dict: dict[str, MaterialSupply], notifications: List[MaterialNotification]):
        for notification in notifications:
            supply = supplies_dict.get(notification.code)
            if supply:
                notification.shipped_available = notification.shipped - supply.supplied

    def execute(self):
        supplies = self._supply_repository.get_by_root_id(self._root.root_id)
        supplies_dict = {x.code: x for x in supplies}
        notifications = self._material_notification_repository.get()
        # supplies = list(filter(lambda x: x.code in notifications, supplies))
        # notifications = list(filter(lambda x: x.passed_date and x.code in supplies, notifications))
        self._calculate(supplies_dict, notifications)
