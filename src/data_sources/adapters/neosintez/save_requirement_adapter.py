from typing import List
from ...gateways import neosintez
from domain.entities import MaterialRequirement
from .abstract_adapter import AbstractAdapter


class SaveRequirementAdapter(AbstractAdapter):

    def _get_request_body(self, item: MaterialRequirement):
        request_body = []
        request_body.extend([
            {
                'Name': 'forvalidation',
                'Value': item.new_issued if item.new_issued else None,
                'Type': 1,
                'Id': self.requirement_issued_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_supplied if item.new_supplied else None,
                'Type': 1,
                'Id': self.requirement_supplied_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_supply_amount if item.new_supply_amount else None,
                'Type': 1,
                'Id': self.requirement_supply_amount_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_available if item.new_available else None,
                'Type': 1,
                'Id': self.available_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_rest_total_available if item.new_rest_total_available else None,
                'Type': 1,
                'Id': self.rest_total_available_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_rest_available if item.new_rest_available else None,
                'Type': 1,
                'Id': self.rest_available_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_free_available if item.new_free_available else None,
                'Type': 1,
                'Id': self.free_available_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_free_total_available if item.new_free_total_available else None,
                'Type': 1,
                'Id': self.free_total_available_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_total_delivered if item.new_total_delivered else None,
                'Type': 1,
                'Id': self.total_delivered_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_total_moving if item.new_total_moving else None,
                'Type': 1,
                'Id': self.total_moving_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_moving if item.new_moving else None,
                'Type': 1,
                'Id': self.moving_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_delivered if item.new_delivered else None,
                'Type': 1,
                'Id': self.delivered_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.name,
                'Type': 2,
                'Id': self.requirement_name_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_shipped_available if item.new_shipped_available else None,
                'Type': 1,
                'Id': self.shipped_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_shipped_total_available if item.new_shipped_total_available else None,
                'Type': 1,
                'Id': self.total_shipped_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_codes_string if item.new_codes_string else None,
                'Type': 6,
                'Id': self.codes_string_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_supply_request if item.new_supply_request else None,
                'Type': 2,
                'Id': self.supply_request_list_attribute_id
            },
            {
                'Name': 'forvalidation',
                'Value': item.new_max_date.strftime('%Y-%m-%d') if item.new_max_date else None,
                'Type': 3,
                'Id': self.requirement_date_attribute_id
            }
        ])

        return request_body

    def _get_payloads(self, items):
        payloads = list()
        for item in items:
            request_body = self._get_request_body(item)
            payloads.append(
                {
                    'route': f'/api/objects/{item.item_id}/attributes',
                    'request_body': request_body,
                }
            )
        return payloads

    def execute(self, items: List[MaterialRequirement]) -> dict:
        """Метод принимает список экземпляров MaterialRequirement.
                Возвращает dict со счетчиками с ключами success и error со значениями int"""
        payloads = self._get_payloads(items)
        result = {'success': 0, 'error': 0}
        responses = neosintez.MakeRequests.execute(payloads, self._session, 'put')
        for response in responses:
            if response['status'] == 200:
                result['success'] += 1
            else:
                result['error'] += 1

        return result
