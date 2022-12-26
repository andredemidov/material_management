from domain.entities import Root
from domain.use_cases.get_related_materials_instances import GetRelatedMaterialsInstances
from domain.use_cases.mark_duplicated_related_materials import MarkDuplicatedRelatedMaterials
from domain.use_cases.normalize_related_materials import NormalizeRelatedMaterials


class NormalizeForRoot:

    def __init__(self, requirement_repository, related_material_repository, root: Root, log_adapter):
        self._requirement_repository = requirement_repository
        self._related_material_repository = related_material_repository
        self._root = root
        self._log_adapter = log_adapter

    def info(self) -> str:
        return f'normalizing {self._root.name}'

    def execute(self):
        log = self._log_adapter
        log.write_info('Getting instances of entities')
        GetRelatedMaterialsInstances(self._requirement_repository, self._related_material_repository, self._root).execute()

        # пометка дублей на удаление и их удаление
        MarkDuplicatedRelatedMaterials(self._requirement_repository).execute()
        log.write_info('Deleting related materials')
        responses_statistic = self._related_material_repository.delete_marked_for_delete()
        count_success = responses_statistic["success"]
        count_error = responses_statistic["error"]
        log.write_info(f'Deleting related materials complete. Success {count_success}, error {count_error}')

        log.write_info('Normalizing')
        NormalizeRelatedMaterials(self._requirement_repository).execute()
        log.write_info('Creating related materials')
        responses_statistic = self._related_material_repository.create()
        count_success = responses_statistic["success"]
        count_error = responses_statistic["error"]
        log.write_info(f'Creating related materials complete. Success {count_success}, error {count_error}')
