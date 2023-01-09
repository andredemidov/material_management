from domain.entities import Root

from domain.use_cases.get_related_materials_instances import GetRelatedMaterialsInstances
from domain.use_cases.get_related_material_supply_instances import GetRelatedMaterialSupplyInstances
from domain.use_cases.get_related_material_order_instance import GetRelatedMaterialOrderInstances
from domain.use_cases.get_related_material_notification_instance import GetRelatedMaterialNotificationInstances
from domain.use_cases.mark_duplicated_related_materials import MarkDuplicatedRelatedMaterials
from domain.use_cases.get_supply_data_for_requirement import GetSupplyDataForRequirements
from domain.use_cases.calculate_notifications_available import CalculateNotificationsAvailable
from domain.use_cases.set_common_units_notification import SetCommonUnitsNotification
from domain.use_cases.set_common_units_order import SetCommonUnitsOrder
from domain.use_cases.set_common_units_requirement import SetCommonUnitsRequirement
from domain.use_cases.set_common_units_supply import SetCommonUnitsSupply
from domain.use_cases.normalize_related_materials import NormalizeRelatedMaterials


class DistributeForRoot:
    """Вариант использования для распределения поставок по потребностям
    принимает: requirement_repository - репозитории потребностей, related_material_repository - репозиторий
    связанных материалов, replaced_nomenclatures_repository - репозиторий замененных номенклатур,
    main_supply_repository - поставок, order_repository - заказов, root - экземпляр Root,
    log_adapter - адаптер для логирования"""

    def __init__(
            self,
            requirement_repository,
            related_material_repository,
            replaced_nomenclatures_repository,
            main_supply_repository,
            order_repository,
            notification_repository,
            root,
            log_adapter,
    ):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        self._replaced_nomenclatures_repository = replaced_nomenclatures_repository
        self._main_supply_repository = main_supply_repository
        self._order_repository = order_repository
        self._notification_repository = notification_repository
        self._root: Root = root
        self._log_adapter = log_adapter

    def _get_entities_instances(self):
        self._log_adapter.write_info(f'Get related materials called')
        GetRelatedMaterialsInstances(self._requirement_repository, self._related_material_repository, self._root).execute()

    def _add_related_materials_from_replacement_data(self):
        self._log_adapter.write_info(f'Normalizing called')
        NormalizeRelatedMaterials(
            requirement_repository=self._requirement_repository,
            related_material_repository=self._related_material_repository,
            requirement_repository_source=self._replaced_nomenclatures_repository
        ).execute()

    def _set_common_units(self):
        self._log_adapter.write_info(f'Set common units called')
        SetCommonUnitsSupply(self._main_supply_repository).execute()
        SetCommonUnitsRequirement(self._requirement_repository).execute()
        SetCommonUnitsOrder(self._order_repository).execute()
        SetCommonUnitsNotification(self._notification_repository).execute()

    def _delete_duplicated_related_materials(self):
        self._log_adapter.write_info('Deleting related materials')
        MarkDuplicatedRelatedMaterials(self._requirement_repository).execute()
        requirements_with_delete_codes = list(
            filter(lambda item: any(
                map(lambda c: c.delete, item.related_materials)), self._requirement_repository.get_own_supplied_with_main_code())
        )
        self._log_adapter.write_info(f'Total requirements_with_delete_codes {len(requirements_with_delete_codes)}')
        responses_statistic = self._related_material_repository.delete_marked_for_delete()

        # а удаляются ли у меня ссылки на удаляемые экземпляры связанных материалов в атрибуте потребности
        self._log_adapter.write_info(f'Deleting related materials complete')
        self._write_statistic_into_log(responses_statistic)

    def _set_reference_with_supply_data(self):
        self._log_adapter.write_info('Referencing supply data with requirements')
        CalculateNotificationsAvailable(
            self._notification_repository,
            self._main_supply_repository,
            self._root
        ).execute()
        GetRelatedMaterialOrderInstances(self._requirement_repository, self._order_repository).execute()
        GetRelatedMaterialNotificationInstances(self._requirement_repository, self._notification_repository).execute()
        GetRelatedMaterialSupplyInstances(self._requirement_repository, self._main_supply_repository).execute()
        GetSupplyDataForRequirements(self._requirement_repository).execute()

    def _save_requirements(self):
        changed_requirements = list(filter(lambda x: x.have_change(), self._requirement_repository.get_own_supplied_with_main_code()))
        self._log_adapter.write_info(f'Total changed requirements {len(changed_requirements)}')
        responses_statistic = self._requirement_repository.save()
        self._log_adapter.write_info(f'Saving requirements complete')
        self._write_statistic_into_log(responses_statistic)

    def _create_new_related_materials(self):
        self._log_adapter.write_info('Creating related materials')
        responses_statistic = self._related_material_repository.create()
        self._log_adapter.write_info(
            f'Creating related materials complete')
        self._write_statistic_into_log(responses_statistic)

    def _save_related_materials(self):
        self._log_adapter.write_info('Saving related materials')
        responses_statistic = self._related_material_repository.save()
        self._log_adapter.write_info(f'Save related materials complete')
        self._write_statistic_into_log(responses_statistic)

    def _write_statistic_into_log(self, statistic: dict):
        count_success = statistic["success"]
        count_error = statistic["error"]
        self._log_adapter.write_info(f'Success {count_success}, error {count_error}')

    def info(self) -> str:
        return f'distribution {self._root.name}'

    def execute(self):
        self._get_entities_instances()
        self._add_related_materials_from_replacement_data()
        self._set_common_units()
        self._delete_duplicated_related_materials()
        self._set_reference_with_supply_data()
        self._save_requirements()
        self._create_new_related_materials()
        self._save_related_materials()
