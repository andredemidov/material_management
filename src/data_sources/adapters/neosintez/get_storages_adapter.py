from domain.entities import Root, MaterialStorage
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetStoragesAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._storages_data: list = list()
        self._storages: list[MaterialStorage] = list()

    def _get_storages_data(self, root_id):
        print('get orders is called')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.storages_class_id
                }
            ],
            "Conditions": [
                {
                    "Type": 1,
                    "Attribute": self.delete_attribute_id,
                    "Operator": 1,
                    "Value": self.delete_attribute_value
                },
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
            self._storages_data.extend(result['data']['Result'])
        print('response of storages is got', len(self._storages_data))

    def _init_storages(self, item):

        attributes = item['Object']['Attributes']
        code = self.get_value(attributes, self.code_attribute_id)
        unit = self.get_value(attributes, self.unit_attribute_id)
        reserved = self.get_value(attributes, self.amount_attribute_id, attribute_type='int')
        storage_id = self.get_value(attributes, self.storage_id_attribute_id)
        name = self.get_value(attributes, self.name_attribute_id)

        next_storage = MaterialStorage(
            code=code,
            reserved=reserved,
            storage_id=storage_id,
            unit=unit,
            name=name,
        )
        if next_storage in self._storages:
            index = self._storages.index(next_storage)
            exist_storage = self._storages[index]
            exist_storage.reserved += next_storage.reserved

            self._storages[index] = exist_storage
        else:
            self._storages.append(next_storage)

    def execute(self, root: Root) -> list[MaterialStorage]:
        self._get_storages_data(root.root_id)
        for item in self._storages_data:
            self._init_storages(item)
        return self._storages
