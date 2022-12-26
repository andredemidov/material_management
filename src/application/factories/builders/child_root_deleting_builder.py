from domain.repositories import RequirementRepository, RelatedMaterialRepository
from domain.interactors import DeleteForRoot
from domain.entities import Root
from utilites.write_log_message_adapter import WriteLogMessageAdapter


class ChildRootDeletingBuilder:

    def __call__(self, child_root: Root, get_adapter, post_adapter, **_ignored):

        requirement_repository = RequirementRepository(
            get_data_adapter=get_adapter,
            post_data_adapter=post_adapter,
            root=child_root
        )
        related_material_repository = RelatedMaterialRepository(
            get_data_adapter=get_adapter,
            post_data_adapter=post_adapter,
            root=child_root
        )
        log_adapter = WriteLogMessageAdapter()
        delete_for_root = DeleteForRoot(
            requirement_repository=requirement_repository,
            related_material_repository=related_material_repository,
            root=child_root,
            log_adapter=log_adapter,
        )
        return delete_for_root
