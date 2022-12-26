from domain.entities import Root
from .abstract_adapter import AbstractAdapter
from data_sources.gateways.neosintez import GetTotal


class GetRootDeleteStatusAdapter(AbstractAdapter):

    def _get_request_body(self, root_id):

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
            ],
            "Conditions": [
                {
                    "Type": 1,
                    "Direction": 0,
                    "Operator": 7,
                    "Logic": 0,
                    "Attribute": self.code_attribute_id,
                },
                {
                    "Type": 1,
                    "Direction": 1,
                    "Operator": 1,
                    "Logic": 2,
                    "Value": self.delete_attribute_value,
                    "Attribute": self.delete_attribute_id
                }
            ]
        }
        return payload

    def execute(self, root: Root) -> bool:
        request_body = self._get_request_body(root.root_id)
        results = GetTotal.execute(request_body, self._session)
        return bool(results)
