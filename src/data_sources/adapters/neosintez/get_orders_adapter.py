from typing import List
from domain.entities import Root, MaterialOrder
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetOrdersAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._orders_data = list()
        self._orders = list()

    def _get_orders_data(self, root_id):
        print('get orders is called')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.order_class_id
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
            self._orders_data.extend(result['data']['Result'])
        print('response of orders is got', len(self._orders_data))

    def _init_orders(self, item):

        attributes = item['Object']['Attributes']
        code = self.get_value(attributes, self.code_attribute_id)
        unit = self.get_value(attributes, self.unit_attribute_id)
        moving = self.get_value(attributes, self.moving_attribute_id, attribute_type='int')
        delivered = self.get_value(attributes, self.delivered_attribute_id, attribute_type='int')
        contractor_id = self.get_value(attributes, self.contractor_attribute_id, get_only_id=True)
        creation_date = self.get_value(attributes, self.order_creation_date_attribute_id)

        next_order = MaterialOrder(
            code=code,
            contractor_id=contractor_id,
            moving=moving,
            delivered=delivered,
            creation_date=creation_date,
            unit=unit,
        )
        if next_order in self._orders:
            index = self._orders.index(next_order)
            exist_order = self._orders[index]
            exist_order.moving += next_order.moving
            exist_order.delivered += next_order.delivered

            self._orders[index] = exist_order
        else:
            self._orders.append(next_order)

    def execute(self, root: Root) -> List[MaterialOrder]:
        self._get_orders_data(root.root_id)
        for item in self._orders_data:
            self._init_orders(item)
        return self._orders
