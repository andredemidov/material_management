from typing import List
from ...gateways import neosintez
from domain.entities import MaterialRelated
from .abstract_adapter import AbstractAdapter


class CreateRelatedMaterialAdapter(AbstractAdapter):

    def _get_request_body(self, item: MaterialRelated):
        request_body = {
            "Id": "00000000-0000-0000-0000-000000000000",
            "Name": "forvalidation",
            "Entity": {
                "Id": self.related_material_class_id,
                "Name": "forvalidation"
            },
            "Attributes": {
                self.code_attribute_id: {
                    "Id": self.code_attribute_id,
                    "Name": "forvalidation",
                    "Type": 2,
                    "Value": item.code,
                }
            }
        }
        return request_body

    def _get_payloads(self, items):
        payloads = list()
        for item in items:
            request_body = self._get_request_body(item)
            payloads.append(
                {
                    'route': f'/api/objects/{item.host}/collections?attributeId={self.collection_attribute_id}',
                    'request_body': request_body,
                }
            )
        return payloads

    def _set_self_id_for_created(self, items: List[MaterialRelated], responses):
        responses = list(filter(lambda x: x['status'] == 200, responses))
        self_ids = dict(map(lambda x: (x['data']['Object']['Attributes'][self.code_attribute_id]['Value'], x['data']['Object']['Id']), responses))
        for item in items:
            item.self_id = self_ids.get(item.code)

    def execute(self, items: List[MaterialRelated]) -> dict:
        """Метод принимает список экземпляров MaterialRelated.
                Возвращает dict со счетчиками с ключами success и error со значениями int"""

        result = {'success': 0, 'error': 0}
        payloads = self._get_payloads(items)
        responses = neosintez.MakeRequests.execute(payloads, self._session, 'post')
        self._set_self_id_for_created(items, responses)
        for response in responses:
            if response['status'] == 200:
                result['success'] += 1
            else:
                result['error'] += 1

        return result
