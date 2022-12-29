from domain.repositories import RequirementRepository, RelatedMaterialRepository
from domain.interactors import ValidateRelatedMaterialsForRoot
from domain.entities import Root
from utilites.write_log_message_adapter import WriteLogMessageAdapter


class ChildRootRelatedMaterialsValidatingBuilder:

    def __call__(self, child_root: Root, get_adapter, post_adapter, supply_repository, **_ignored):

        requirement_repository = RequirementRepository(
            post_data_adapter=post_adapter,
            get_data_adapter=get_adapter,
            root=child_root,
        )
        related_material_repository = RelatedMaterialRepository(
            post_data_adapter=post_adapter,
            get_data_adapter=get_adapter,
            root=child_root,
        )
        log_adapter = WriteLogMessageAdapter()

        normalize_for_root = ValidateRelatedMaterialsForRoot(
            requirement_repository=requirement_repository,
            related_material_repository=related_material_repository,
            main_supply_repository=supply_repository,
            root=child_root,
            log_adapter=log_adapter,
        )
        return normalize_for_root
