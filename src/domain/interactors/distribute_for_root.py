from domain.entities import Root
from domain import use_cases


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
            storages_repository,
            root,
            log_adapter,
    ):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        self._replaced_nomenclatures_repository = replaced_nomenclatures_repository
        self._main_supply_repository = main_supply_repository
        self._order_repository = order_repository
        self._notification_repository = notification_repository
        self._storages_repository = storages_repository
        self._root: Root = root
        self._log_adapter = log_adapter

    def _get_entities_instances(self):
        self._log_adapter.write_info(f'Get related materials called')
        use_cases.GetRelatedMaterialsInstances(
            self._requirement_repository,
            self._related_material_repository,
            self._root
        ).execute()

    def _validate_related_materials_names(self):
        self._log_adapter.write_info(f'Validation related materials called')
        use_cases.ValidateRelatedMaterialsName(self._requirement_repository)

    def _add_related_materials_from_replacement_data(self):
        self._log_adapter.write_info(f'Normalizing called')
        use_cases.NormalizeRelatedMaterials(
            requirement_repository=self._requirement_repository,
            related_material_repository=self._related_material_repository,
            requirement_repository_source=self._replaced_nomenclatures_repository
        ).execute()

    def _set_common_units(self):
        self._log_adapter.write_info(f'Set common units called')
        use_cases.set_common_units.SetCommonUnitsSupply(self._main_supply_repository).execute()
        use_cases.set_common_units.SetCommonUnitsRequirement(self._requirement_repository).execute()
        use_cases.set_common_units.SetCommonUnitsOrder(self._order_repository).execute()
        use_cases.set_common_units.SetCommonUnitsNotification(self._notification_repository).execute()
        use_cases.set_common_units.SetCommonUnitsStorage(self._storages_repository).execute()

    def _set_reference_with_supply_data(self):
        self._log_adapter.write_info('Join supply data with requirements')
        use_cases.CalculateNotificationsAvailable(
            self._notification_repository,
            self._main_supply_repository,
            self._root
        ).execute()
        use_cases.GetRelatedMaterialOrderInstances(self._requirement_repository, self._order_repository).execute()
        use_cases.GetRelatedMaterialNotificationInstances(
            self._requirement_repository,
            self._notification_repository
        ).execute()
        use_cases.GetRelatedMaterialSupplyInstances(
            self._requirement_repository,
            self._main_supply_repository
        ).execute()
        use_cases.GetRelatedMaterialStorageInstances(self._requirement_repository, self._storages_repository).execute()
        use_cases.GetSupplyDataForRequirements(self._requirement_repository, only_valid=False).execute()

    def _set_mating_part_status(self):
        self._log_adapter.write_info('Check if mating part exist')
        use_cases.CheckIfMatingPartExist(self._requirement_repository).execute()

    def _save_requirements(self):
        changed_requirements = list(
            filter(lambda x: x.have_change(), self._requirement_repository.get_own_supplied_with_main_code()))
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
        if count_error:
            self._log_adapter.write_warning(f'Success {count_success}, error {count_error}')
        else:
            self._log_adapter.write_info(f'Success {count_success}, error {count_error}')

    def info(self) -> str:
        return f'distribution {self._root.name}'

    def execute(self):
        self._get_entities_instances()
        self._add_related_materials_from_replacement_data()
        self._set_common_units()
        self._set_reference_with_supply_data()
        self._set_mating_part_status()
        self._save_requirements()
        self._create_new_related_materials()
        self._save_related_materials()
