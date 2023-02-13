from domain.repositories import RequirementRepository, SupplyRepository, OrderRepository, NotificationRepository, \
    RelatedMaterialRepository, ReplacedNomenclaturesRepository, StoragesRepository
from domain.interactors import DistributeForRoot
from domain.entities import Root
from utilites.write_log_message_adapter import WriteLogMessageAdapter


class ChildRootDistributionBuilder:

    def __call__(self, child_root: Root, get_adapter, post_adapter, supply_repository: SupplyRepository, **_ignored):

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
        replaced_nomenclatures_repository = ReplacedNomenclaturesRepository(get_data_adapter=get_adapter)
        order_repository = OrderRepository(get_data_adapter=get_adapter, root=child_root)
        notification_repository = NotificationRepository(get_data_adapter=get_adapter, root=child_root)
        storages_repository = StoragesRepository(get_data_adapter=get_adapter, root=child_root)
        new_supply_repository = supply_repository.copy()
        log_adapter = WriteLogMessageAdapter()

        distribute_for_root = DistributeForRoot(
            requirement_repository=requirement_repository,
            related_material_repository=related_material_repository,
            replaced_nomenclatures_repository=replaced_nomenclatures_repository,
            order_repository=order_repository,
            notification_repository=notification_repository,
            storages_repository=storages_repository,
            main_supply_repository=new_supply_repository,
            root=child_root,
            log_adapter=log_adapter,
        )
        return distribute_for_root
