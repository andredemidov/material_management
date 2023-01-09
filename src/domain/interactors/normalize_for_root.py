from domain.entities import Root
from domain.use_cases.get_related_materials_instances import GetRelatedMaterialsInstances
from domain.use_cases.mark_duplicated_related_materials import MarkDuplicatedRelatedMaterials
from domain.use_cases.mark_related_material_for_delete import MarkRelatedMaterialForDelete
from domain.use_cases.normalize_related_materials import NormalizeRelatedMaterials
from domain.use_cases.validate_related_materials_name import ValidateRelatedMaterialsName
from domain.use_cases.get_related_material_supply_instances import GetRelatedMaterialSupplyInstances


class NormalizeForRoot:

    def __init__(
            self,
            requirement_repository,
            related_material_repository,
            main_supply_repository,
            root: Root,
            log_adapter
    ):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        self._main_supply_repository = main_supply_repository
        self._root = root
        self._log_adapter = log_adapter

    def info(self) -> str:
        return f'normalizing {self._root.name}'

    def execute(self):
        log = self._log_adapter
        log.write_info('Getting instances of entities')
        GetRelatedMaterialsInstances(
            self._requirement_repository,
            self._related_material_repository,
            self._root
        ).execute()

        MarkDuplicatedRelatedMaterials(self._requirement_repository).execute()
        MarkRelatedMaterialForDelete(self._requirement_repository).execute()

        GetRelatedMaterialSupplyInstances(self._requirement_repository, self._main_supply_repository).execute()

        log.write_info(f'Validating nomenclatures in comparison with host requirements')
        ValidateRelatedMaterialsName(self._requirement_repository).execute()
        log.write_info('Validating complete')

        log.write_info('Normalizing')
        NormalizeRelatedMaterials(
            requirement_repository=self._requirement_repository,
            related_material_repository=self._related_material_repository,
        ).execute()

        log.write_info('Creating related materials')
        responses_statistic = self._related_material_repository.create()
        count_success = responses_statistic["success"]
        count_error = responses_statistic["error"]
        log.write_info(f'Creating related materials complete. Success {count_success}, error {count_error}')

        log.write_info('Saving validation info of related materials')
        responses_statistic = self._related_material_repository.save(only_validation_info=True)
        count_success = responses_statistic["success"]
        count_error = responses_statistic["error"]
        log.write_info(
            f'Saving validation info related materials complete. Success {count_success}, error {count_error}')
