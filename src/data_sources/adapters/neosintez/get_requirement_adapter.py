from typing import List
from domain.entities import Root, MaterialRequirement
from data_sources.gateways.neosintez import MakeSearchRequests

from .abstract_adapter import AbstractAdapter


class GetRequirementAdapter(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)
        self._requirements_data = list()
        self._requirements = list()

    def _get_requirements_data(self, root_id):
        print('get_reqs is called')
        payload = {
            "Filters": [
                {
                    "Type": 4,
                    "Value": root_id
                },
                {
                    "Type": 5,
                    "Value": self.requirement_class_id
                }
            ],
            "Conditions": [
                {
                    "Type": 1,
                    # "Direction": 1,
                    # "Logic": 0,
                    "Attribute": self.actual_attribute_id,
                    "Operator": 1,
                    "Value": self.actual_attribute_value
                },
                # {
                #     "Type": 1,
                #     "Attribute": self.code_attribute_id,
                #     "Operator": 7,
                #     "Direction": 1,
                #     "Logic": 2,
                # },
                # {
                #     'Value': self.type_supply_attribute_value,
                #     "Type": 1,
                #     "Attribute": self.type_supply_attribute_id,
                #     "Operator": 2,
                #     "Direction": 1,
                #     "Logic": 2,
                #     "Group": '1',
                # },
                # {
                #     "Type": 1,
                #     "Attribute": self.type_supply_attribute_id,
                #     "Operator": 8,
                #     "Direction": 1,
                #     "Logic": 1,
                #     "Group": '1',
                # },
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
            self._requirements_data.extend(result['data']['Result'])

    def _init_requirement(self, item):
        attributes = item['Object']['Attributes']
        item_id = item['Object']['Id']
        name = self.get_value(attributes, self.requirement_name_attribute_id).strip()
        item_type = self.get_value(attributes, self.type_attribute_id)
        main_code = self.get_value(attributes, self.code_attribute_id)
        # code_string = self.get_value(attributes, self.code_string_attribute_id)
        level_4 = self.get_value(attributes, self.level_4_attribute_id)
        level_3 = self.get_value(attributes, self.level_3_attribute_id)
        project_section = self.get_value(attributes, self.project_section_attribute_id)
        axes = self.get_value(attributes, self.axes_attribute_id)
        amount = self.get_value(attributes, self.amount_attribute_id, attribute_type='int')
        weld = self.get_value(attributes, self.weld_attribute_id, attribute_type='int')
        one_mass = self.get_value(attributes, self.mass_attribute_id, attribute_type='int')
        priority = self.get_value(attributes, self.priority_attribute_id)
        plan_date = self.get_value(attributes, self.plan_date_attribute_id, attribute_type='date')
        mounted = self.get_value(attributes, self.mounted_attribute_id, attribute_type='int')
        mounted_spool = self.get_value(attributes, self.mounted_spool_attribute_id, attribute_type='int')
        construction = self.get_value(attributes, self.construction_attribute_id)
        construction_object = self.get_value(attributes, self.construction_object_attribute_id)
        construction_subobject = self.get_value(attributes, self.construction_subobject_attribute_id)
        contractor_id = self.get_value(attributes, self.contractor_attribute_id, get_only_id=True)
        contractor = self.get_value(attributes, self.contractor_attribute_id)
        unit = self.get_value(attributes, self.unit_attribute_id)
        diameter = self.get_value(attributes, self.diameter_attribute_id, attribute_type='int')
        type_supply = self.get_value(attributes, self.type_supply_attribute_id)
        type_supply = type_supply if type_supply else 'Заказчик'

        requirement = MaterialRequirement(
            item_id=item_id,
            main_code=main_code,
            name=name,
            one_mass=one_mass,
            type=item_type,
            type_supply=type_supply,
            level_4=level_4,
            level_3=level_3,
            project_section=project_section,
            amount=amount,
            weld=weld,
            unit=unit,
            diameter=diameter,
            construction=construction,
            construction_object=construction_object,
            construction_subobject=construction_subobject,
            contractor_id=contractor_id,
            contractor=contractor,
            axes=axes,
            priority=priority,
            plan_date=plan_date,
            mounted=mounted,
            mounted_spool=mounted_spool,
        )
        self._requirements.append(requirement)
        self._get_current_distributing_data(item, requirement)

    def _get_current_distributing_data(self, item, requirement: MaterialRequirement):
        attributes = item['Object']['Attributes']
        requirement.cur_supply_amount = self.get_value(
            attributes,
            self.requirement_supply_amount_attribute_id,
            attribute_type='int'
        )
        requirement.cur_issued = self.get_value(
            attributes,
            self.requirement_issued_attribute_id,
            attribute_type='int'
        )
        requirement.cur_supplied = self.get_value(
            attributes,
            self.requirement_supplied_attribute_id,
            attribute_type='int'
        )
        requirement.cur_moving = self.get_value(
            attributes,
            self.moving_attribute_id,
            attribute_type='int'
        )
        requirement.cur_total_moving = self.get_value(
            attributes,
            self.total_moving_attribute_id,
            attribute_type='int'
        )
        requirement.cur_total_delivered = self.get_value(
            attributes,
            self.total_delivered_attribute_id,
            attribute_type='int'
        )
        requirement.cur_delivered = self.get_value(
            attributes,
            self.delivered_attribute_id,
            attribute_type='int'
        )
        requirement.cur_shipped_available = self.get_value(attributes, self.shipped_attribute_id, attribute_type='int')
        requirement.cur_shipped_total_available = self.get_value(
            attributes,
            self.total_shipped_attribute_id,
            attribute_type='int'
        )
        requirement.cur_available = self.get_value(
            attributes,
            self.requirement_available_attribute_id,
            attribute_type='int'
        )
        requirement.cur_rest_total_available = self.get_value(
            attributes,
            self.rest_total_available_attribute_id,
            attribute_type='int'
        )
        requirement.cur_rest_available = self.get_value(
            attributes,
            self.rest_available_attribute_id,
            attribute_type='int'
        )
        requirement.cur_free_available = self.get_value(
            attributes,
            self.free_available_attribute_id,
            attribute_type='int'
        )
        requirement.cur_free_total_available = self.get_value(
            attributes,
            self.free_total_available_attribute_id,
            attribute_type='int'
        )
        requirement.cur_max_date = self.get_value(
            attributes,
            self.requirement_date_attribute_id,
            attribute_type='date'
        )
        requirement.cur_codes_string = self.get_value(
            attributes,
            self.codes_string_attribute_id,
        )
        requirement.cur_supply_request = self.get_value(
            attributes,
            self.supply_request_list_attribute_id,
        )

    def execute(self, root: Root) -> List[MaterialRequirement]:
        self._get_requirements_data(root_id=root.root_id)
        print('response of requirements got', len(self._requirements_data))
        for item in self._requirements_data:
            self._init_requirement(item)
        return self._requirements
