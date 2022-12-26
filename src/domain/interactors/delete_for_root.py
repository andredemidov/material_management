from domain.entities import Root
from domain.use_cases.get_related_materials_instances import GetRelatedMaterialsInstances
from domain.use_cases.mark_duplicated_related_materials import MarkDuplicatedRelatedMaterials
from domain.use_cases.mark_related_material_for_delete import MarkRelatedMaterialForDelete


class DeleteForRoot:

    def __init__(self, requirement_repository, related_material_repository, root: Root, log_adapter):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        self._root = root
        self._log_adapter = log_adapter

    def info(self) -> str:
        return f'deleting {self._root.name}'

    def execute(self):
        log = self._log_adapter
        need_for_delete = self._requirement_repository.check_if_marked_for_delete_is_exist()
        if not need_for_delete:
            log.write_info('Delete needing is false')
            return None
        log.write_info('Getting instances of entities')
        GetRelatedMaterialsInstances(self._requirement_repository, self._related_material_repository, self._root).execute()

        MarkRelatedMaterialForDelete(self._requirement_repository).execute()
        MarkDuplicatedRelatedMaterials(self._requirement_repository).execute()
        log.write_info('Deleting related materials')
        requirements_with_delete_codes = list(
            filter(lambda item: any(
                map(lambda c: c.delete, item.related_materials)), self._requirement_repository.get_customer_supplied_with_main_code())
        )
        log.write_info(f'Total requirements_with_delete_codes {len(requirements_with_delete_codes)}')
        responses_statistic = self._related_material_repository.delete_marked_for_delete()
        count_success = responses_statistic["success"]
        count_error = responses_statistic["error"]
        log.write_info(f'Deleting related materials complete. Success {count_success}, error {count_error}')
