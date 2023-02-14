from domain.entities import MaterialRequirement


class GetRelatedMaterialNotificationInstances:

    def __init__(self, requirement_repository, material_notification_repository):
        self._requirement_repository = requirement_repository
        self._material_notification_repository = material_notification_repository

    @staticmethod
    def _find_notification_material(requirement: MaterialRequirement, notifications_codes: dict):
        for related_material in requirement.related_materials:
            related_material.notification = notifications_codes.get(related_material.code)

    def execute(self):
        notifications = self._material_notification_repository.get()
        notifications_codes = {x.code: x for x in notifications}

        for requirement in self._requirement_repository.get_own_supplied_with_main_code():
            self._find_notification_material(requirement, notifications_codes)
        print('get notification materials instances complete')
