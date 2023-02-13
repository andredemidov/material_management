from typing import List
from domain.entities import Root
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetRootsAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._roots_data = list()
        self._roots = list()

    def _get_child_roots_data(self, root_id):
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.child_root_class_id
                }
            ]
        }
        payloads = [
            {
                'route': '',
                'request_body': payload,
            }
        ]
        results = MakeSearchRequests.execute(payloads, self._session, 'post')
        for result in results:
            if result['status'] != 200:
                message = f"one or more search requests have status not equal 200. {result['data']}"
                raise RuntimeError(message)
            self._roots_data.extend(result['data']['Result'])
        print('response of root is got', len(self._roots_data))

    def _get_main_roots_data(self):
        payload = {
            "Filters": [
                {
                    "Type": 5,
                    "Value": self.main_root_class_id
                }
            ]
        }
        payloads = [
            {
                'route': '',
                'request_body': payload,
            }
        ]
        results = MakeSearchRequests.execute(payloads, self._session, 'post')
        for result in results:
            if result['status'] != 200:
                message = f"one or more search requests have status not equal 200. {result['data']}"
                raise RuntimeError(message)
            self._roots_data.extend(result['data']['Result'])
        print('response of root is got', len(self._roots_data))

    def _init_roots(self, item, parent_root_id):

        attributes = item['Object']['Attributes']
        root_id = item['Object']['Id']
        name = item['Object']['Name']
        construction_object = self.get_value(attributes, self.construction_object_attribute_id)
        cost_center_code = self.get_value(attributes, self.cost_center_code_attribute_id)

        root = Root(
            name=name,
            root_id=root_id,
            parent_root=parent_root_id,
            construction_object=construction_object,
            cost_center_code=cost_center_code,
        )
        onsite_storage_ids = self.get_value(attributes, self.onsite_storages_attribute_id)
        if onsite_storage_ids:
            onsite_storage_ids = [x.strip() for x in onsite_storage_ids.split(';')]
            root.onsite_storage_ids = onsite_storage_ids
        self._roots.append(root)

    def execute(self, root: Root = None) -> List[Root]:
        print('get roots is called')
        root_id = root.root_id if root else None
        if root:
            self._get_child_roots_data(root_id)
        else:
            self._get_main_roots_data()

        for item in self._roots_data:
            self._init_roots(item, root_id)
        return self._roots
