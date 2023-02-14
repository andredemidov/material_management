from typing import List
from domain.entities import Root, MaterialOrder, MaterialRequirement, MaterialRelated, MaterialSupply, \
    MaterialNotification, ReplacedNomenclature, MaterialStorage
from data_sources.adapters import neosintez, excel, memcached


class GetDataAdapterFacade:

    def __init__(self, session, codes_replacement_file_path=None):
        self._session = session
        self._codes_replacement_file_path = codes_replacement_file_path

    def get_requirements(self, root: Root) -> List[MaterialRequirement]:
        return neosintez.GetRequirementAdapter(self._session).execute(root)

    def get_supplies(self, main_root: Root) -> List[MaterialSupply]:
        result = memcached.GetSupplyDataAdapter.execute(main_root)
        if not result:
            child_roots = self.get_child_roots(main_root)
            for child_root in child_roots:
                result.extend(neosintez.GetSuppliesAdapter(self._session).execute(child_root))
            result.extend(neosintez.GetSuppliesAdapter(self._session).execute(main_root))
            memcached.CacheRequirementDataAdapter.execute(main_root, result)
        return result

    def get_supplies_by_child_root(self, child_root: Root) -> List[MaterialSupply]:
        main_root = neosintez.GetMainRootByChild(self._session).execute(child_root)
        return self.get_supplies(main_root)

    def get_another_supplies(self, root: Root) -> List[MaterialSupply]:
        return neosintez.GetSuppliesAdapter(self._session).execute(root)

    def get_orders(self, root: Root) -> List[MaterialOrder]:
        return neosintez.GetOrdersAdapter(self._session).execute(root)

    def get_notifications(self, root: Root, date=None) -> List[MaterialNotification]:
        return neosintez.GetNotificationsAdapter(self._session).execute(root, date)

    def get_related_materials(self, root: Root) -> List[MaterialRelated]:
        return neosintez.GetRelatedMaterialAdapter(self._session).execute(root)

    def get_storages(self, root: Root) -> List[MaterialStorage]:
        return neosintez.GetStoragesAdapter(self._session).execute(root)

    def get_child_roots(self, parent_root: Root) -> List[Root]:
        return neosintez.GetRootsAdapter(self._session).execute(parent_root)

    def get_child_roots_by_child_root(self, child_root: Root) -> (List[Root], Root):
        main_root = neosintez.GetMainRootByChild(self._session).execute(child_root)
        return self.get_child_roots(main_root), main_root

    def get_main_roots(self) -> List[Root]:
        return neosintez.GetRootsAdapter(self._session).execute()

    def get_delete_status(self, root: Root) -> bool:
        return neosintez.GetRootDeleteStatusAdapter(self._session).execute(root)

    def get_replaced_nomenclatures(self) -> List[ReplacedNomenclature]:
        return excel.GetReplacedNomenclatureAdapter(self._codes_replacement_file_path).execute()
