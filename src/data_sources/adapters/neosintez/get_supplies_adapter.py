from typing import List
from domain.entities import Root, MaterialSupply
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetSuppliesAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._supplies_data = list()
        self._supplies = list()

    def _get_supplies_data(self, root_id):
        print('get supplies is called')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.supply_class_id
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
            self._supplies_data.extend(result['data']['Result'])
        print('response of supplies is got', len(self._supplies_data))

    def _get_another_supplies_root_id(self, root_id) -> str:
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.free_rest_supplies_folder_class_id
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
        if results:
            one_result = results[0]
            if one_result['status'] == 200 and len(one_result['data']['Result']) > 0:
                print('response of rest_free_root is got', len(one_result['data']['Result']))
                return one_result['data']['Result'][0]['Object']['Id']
        else:
            return ''

    def _check_free(self, attributes: dict) -> bool:
        if self.get_value(attributes, self.title_attribute_id) == 'СО':
            return True
        else:
            return False

    def _init_supply(self, item, root_id, root_name):
        attributes = item['Object']['Attributes']
        code = self.get_value(attributes, self.code_attribute_id)
        amount = self.get_value(attributes, self.supply_amount_attribute_id, attribute_type='int')
        issued = self.get_value(attributes, self.issued_attribute_id, attribute_type='int')
        supplied = self.get_value(attributes, self.supplied_attribute_id, attribute_type='int')
        date = self.get_value(attributes, self.date_attribute_id, attribute_type='date')
        name = self.get_value(attributes, self.name_attribute_id)
        unit = self.get_value(attributes, self.unit_attribute_id)
        supply_request = self.get_value(attributes, self.supply_request_attribute_id)
        root_id = 'free' if self._check_free(attributes) else root_id
        next_supply = MaterialSupply(
            code=code,
            amount=amount,
            unit=unit,
            supply_request={supply_request},
            root_id=root_id,
            root_name=root_name,
            max_date=date,
            issued=issued,
            supplied=supplied,
            name=name,
        )
        if next_supply in self._supplies:
            index = self._supplies.index(next_supply)
            exist_supply = self._supplies[index]
            exist_supply.amount += next_supply.amount
            exist_supply.issued += next_supply.issued
            exist_supply.supplied += next_supply.supplied
            exist_supply.supply_request.update(next_supply.supply_request)
            if next_supply.max_date:
                if not exist_supply.max_date or exist_supply.max_date < next_supply.max_date:
                    exist_supply.max_date = next_supply.max_date

        else:
            self._supplies.append(next_supply)

    def execute(self, root: Root) -> List[MaterialSupply]:
        if root.parent_root:
            root_id = root.root_id
        else:
            root_id = self._get_another_supplies_root_id(root.root_id)

        if root_id:
            self._get_supplies_data(root_id)

            for item in self._supplies_data:
                self._init_supply(item, root_id, root.name)
        return self._supplies
