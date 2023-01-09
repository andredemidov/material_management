from typing import List
from domain.entities import Root, MaterialRelated
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetRelatedMaterialAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._related_materials_data = list()
        self._related_materials = list()

    def _get_related_materials_data(self, root_id: str):
        print('get related is called')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.related_material_class_id
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
            self._related_materials_data.extend(result['data']['Result'])

    def _init_related_material(self, item):
        attributes = item['Object']['Attributes']
        self_id = item['Object']['Id']
        host_id = item['Object']['HostObjectId']
        delete = bool(self.get_value(attributes, self.delete_attribute_id))
        validity_confirmed = self.get_value(attributes, self.valid_attribute_id) == "Корректно имя"
        code = self.get_value(attributes, self.code_attribute_id)
        contractor_id = self.get_value(attributes, self.contractor_attribute_id, get_only_id=True)
        name = self.get_value(attributes, self.name_attribute_id)
        name_valid = self.get_value(attributes, self.valid_attribute_id) not in ("Проверить имя", "Проверить код")

        related_material = MaterialRelated(
            self_id=self_id,
            contractor_id=contractor_id,
            host=host_id,
            code=code,
            delete=delete,
            self_name=name,
            validity_confirmed=validity_confirmed,
            name_valid=name_valid,
        )
        self._related_materials.append(related_material)
        self._get_current_distributing_data(item, related_material)

    def _get_current_distributing_data(self, item, related_material: MaterialRelated):
        attributes = item['Object']['Attributes']
        related_material.cur_available = self.get_value(
            attributes,
            self.available_attribute_id,
            attribute_type='int'
        )
        related_material.cur_free_available = self.get_value(
            attributes,
            self.free_available_attribute_id,
            attribute_type='int'
        )
        related_material.cur_rest_available = self.get_value(
            attributes,
            self.rest_available_attribute_id,
            attribute_type='int'
        )
        related_material.cur_moving = self.get_value(
            attributes,
            self.moving_attribute_id,
            attribute_type='int'
        )
        related_material.cur_delivered = self.get_value(
            attributes,
            self.delivered_attribute_id,
            attribute_type='int'
        )
        related_material.cur_shipped_available = self.get_value(
            attributes,
            self.shipped_attribute_id,
            attribute_type='int'
        )
        related_material.cur_rest_total_available = self.get_value(
            attributes,
            self.rest_total_available_attribute_id,
            attribute_type='int'
        )
        related_material.cur_issued = self.get_value(
            attributes,
            self.requirement_issued_attribute_id,
            attribute_type='int'
        )
        related_material.cur_supplied = self.get_value(
            attributes,
            self.requirement_supplied_attribute_id,
            attribute_type='int'
        )
        related_material.cur_amount = self.get_value(
            attributes,
            self.requirement_supply_amount_attribute_id,
            attribute_type='int'
        )
        related_material.cur_free_total_available = self.get_value(
            attributes,
            self.free_total_available_attribute_id,
            attribute_type='int'
        )
        related_material.cur_total_moving = self.get_value(
            attributes,
            self.total_moving_attribute_id,
            attribute_type='int'
        )
        related_material.cur_total_shipped = self.get_value(
            attributes,
            self.total_shipped_attribute_id,
            attribute_type='int'
        )
        related_material.cur_total_delivered = self.get_value(
            attributes,
            self.total_delivered_attribute_id,
            attribute_type='int'
        )
        related_material.cur_name = self.get_value(attributes, self.name_attribute_id)

        valid_attribute_value = self.get_value(attributes, self.valid_attribute_id)
        related_material.cur_name_valid = valid_attribute_value not in ("Проверить имя", "Проверить код")
        related_material.cur_code_valid = valid_attribute_value != "Проверить код"
        related_material.cur_delete = valid_attribute_value == "Удалить"

    def execute(self, root: Root) -> List[MaterialRelated]:
        self._get_related_materials_data(root_id=root.root_id)

        print('response of related materials is got', len(self._related_materials_data))
        for item in self._related_materials_data:
            self._init_related_material(item)
        return self._related_materials
