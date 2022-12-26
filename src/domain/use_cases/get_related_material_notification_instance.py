from typing import List
from domain.entities import MaterialRequirement, MaterialNotification


class GetRelatedMaterialNotificationInstances:

    def __init__(self, requirement_repository, material_notification_repository):
        self._requirement_repository = requirement_repository
        self._material_notification_repository = material_notification_repository

    @staticmethod
    def _find_notification_material(requirement: MaterialRequirement, notifications_codes: dict):
        for related_material in requirement.related_materials:
            related_material.notification = notifications_codes.get(related_material.code)

    @staticmethod
    def _get_notifications_dict(notifications: List[MaterialNotification]) -> dict:
        """возвращает словарь со структурой {'code': material_notification}"""
        notifications_codes = {}
        for notification_material in notifications:
            notifications_codes[notification_material.code] = notification_material
        return notifications_codes

    def execute(self):
        notifications = self._material_notification_repository.get()
        notifications = list(filter(lambda x: x.passed_date, notifications))
        notifications_codes = self._get_notifications_dict(notifications)

        for requirement in self._requirement_repository.get_customer_supplied_with_main_code():
            self._find_notification_material(requirement, notifications_codes)
        print('get notification materials instances complete')
