from typing import List
from ...gateways import neosintez
from domain.entities import MaterialRelated

from .abstract_adapter import AbstractAdapter


class SaveRelatedMaterialAdapter(AbstractAdapter):

    def _get_request_body(self, item: MaterialRelated, only_validation_info=False):
        request_body = []
        request_body.extend([
            {
                'Name': 'forvalidation',
                'Value': {'Id': self.delete_attribute_value, 'Name': 'forvalidation'} if item.delete else None,
                'Type': 8,
                'Id': self.delete_attribute_id
            },
        ])
        if item.name:
            request_body.append(
                {
                    'Name': 'forvalidation',
                    'Value': item.name,
                    'Type': 2,
                    'Id': self.name_attribute_id
                },
            )
        if item.code_valid is False:
            valid_attribute_value = {'Id': self.valid_attribute_values.get('Проверить код'), 'Name': 'forvalidation'}
        elif item.name_valid is False and item.validity_confirmed is False:
            valid_attribute_value = {'Id': self.valid_attribute_values.get('Проверить имя'), 'Name': 'forvalidation'}
        else:
            valid_attribute_value = None
        if valid_attribute_value:
            request_body.append(
                {
                    'Name': 'forvalidation',
                    'Value': valid_attribute_value,
                    'Type': 8,
                    'Id': self.valid_attribute_id
                }
            )
        if not only_validation_info:

            request_body.extend([
                {
                    'Name': 'forvalidation',
                    'Value': item.free_available if item.free_available else None,
                    'Type': 1,
                    'Id': self.free_available_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.free_total_available if item.free_total_available else None,
                    'Type': 1,
                    'Id': self.free_total_available_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.rest_total_available if item.rest_total_available else None,
                    'Type': 1,
                    'Id': self.rest_total_available_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.rest_available if item.rest_available else None,
                    'Type': 1,
                    'Id': self.rest_available_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.total_moving if item.total_moving else None,
                    'Type': 1,
                    'Id': self.total_moving_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.total_delivered if item.total_delivered else None,
                    'Type': 1,
                    'Id': self.total_delivered_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.delivered if item.delivered else None,
                    'Type': 1,
                    'Id': self.delivered_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.moving if item.moving else None,
                    'Type': 1,
                    'Id': self.moving_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.shipped_available if item.shipped_available else None,
                    'Type': 1,
                    'Id': self.shipped_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.total_shipped if item.total_shipped else None,
                    'Type': 1,
                    'Id': self.total_shipped_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.onsite_storage_available if item.onsite_storage_available else None,
                    'Type': 1,
                    'Id': self.onsite_available_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.remote_storage_available if item.remote_storage_available else None,
                    'Type': 1,
                    'Id': self.remote_available_attribute_id
                },
            ])
            request_body.extend([
                {
                    'Name': 'forvalidation',
                    'Value': item.issued if item.issued else None,
                    'Type': 1,
                    'Id': self.requirement_issued_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.supplied if item.supplied else None,
                    'Type': 1,
                    'Id': self.requirement_supplied_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.amount if item.amount else None,
                    'Type': 1,
                    'Id': self.requirement_supply_amount_attribute_id
                },
                {
                    'Name': 'forvalidation',
                    'Value': item.available if item.available else None,
                    'Type': 1,
                    'Id': self.available_attribute_id
                },
            ])
            if item.contractor_id:
                request_body.append(
                    {
                        'Name': 'forvalidation',
                        'Value': {
                            "Id": item.contractor_id,
                            "Name": "forvalidation"
                        },
                        'Type': 8,
                        'Id': self.contractor_attribute_id
                    },
                )
            else:
                request_body.append(
                    {
                        'Name': 'forvalidation',
                        'Value': {
                            "Name": " "
                        },
                        'Type': 8,
                        'Id': self.contractor_attribute_id
                    },
                )

            if item.supply is not None and item.supply.max_date is not None:
                request_body.append(
                    {
                        'Name': 'forvalidation',
                        'Value': item.supply.max_date.strftime('%Y-%m-%d'),
                        'Type': 3,
                        'Id': self.requirement_date_attribute_id
                    }
                )
            else:
                request_body.append(
                    {
                        'Name': 'forvalidation',
                        'Value': None,
                        'Type': 3,
                        'Id': self.requirement_date_attribute_id
                    }
                )

        return request_body

    def _get_payloads(self, items, only_validation_info=False):
        payloads = list()
        for item in items:
            request_body = self._get_request_body(item, only_validation_info)
            payloads.append(
                {
                    'route': f'/api/objects/{item.self_id}/attributes',
                    'request_body': request_body,
                }
            )
        return payloads

    def execute(self, items: List[MaterialRelated], only_validation_info=False) -> dict:
        """Метод принимает список экземпляров MaterialRelated.
        Возвращает dict со счетчиками с ключами success и error со значениями int"""
        payloads = self._get_payloads(items, only_validation_info)
        result = {'success': 0, 'error': 0}

        responses = neosintez.MakeRequests.execute(payloads, self._session, 'put')
        for response in responses:
            if response['status'] == 200:
                result['success'] += 1
            else:
                result['error'] += 1

        return result
