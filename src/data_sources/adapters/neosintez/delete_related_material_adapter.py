from typing import List
from ...gateways import neosintez
from domain.entities import MaterialRelated
from .abstract_adapter import AbstractAdapter


class DeleteRelatedMaterialAdapter(AbstractAdapter):

    @staticmethod
    def _get_payloads_delete(items):
        payloads = list()
        for related_material in items:
            payloads.append(
                {
                    'route': f'/api/objects/{related_material.host}/collections/{related_material.item_id}',
                    'request_body': '',
                }
            )
        return payloads

    def _get_payloads_get(self, related_materials: List[MaterialRelated]):
        payloads = list()
        hosts = set(map(lambda x: x.host, related_materials))
        for host in hosts:
            attribute_id = self.collection_attribute_id
            payloads.append(
                {
                    'route': f'/api/objects/{host}/collections?attributeId={attribute_id}&Take=100',
                    'request_body': '',
                }
            )
        return payloads

    def execute(self, related_materials: List[MaterialRelated]) -> dict:
        """Метод принимает список экземпляров MaterialRelated.
                        Возвращает dict со счетчиками с ключами success и error со значениями int"""
        result = {'success': 0, 'error': 0}
        if not related_materials:
            return result

        payloads_get = self._get_payloads_get(related_materials)
        responses_get = neosintez.MakeRequests.execute(payloads_get, self._session, 'get')
        print('data of hosts are got')
        # Получить dict вида {self_id: item_id}
        collection_data = {}
        for response in responses_get:
            collection_data.update(dict(map(lambda x: (x['Object']['Id'], x['Id']), response['data']['Result'])))
        for related_material in related_materials:
            related_material.item_id = collection_data[related_material.self_id]

        payloads_delete = self._get_payloads_delete(related_materials)
        responses_delete = neosintez.MakeRequests.execute(payloads_delete, self._session, 'delete')

        for response in responses_delete:
            if response['status'] == 200:
                result['success'] += 1
            else:
                result['error'] += 1

        return result
