import json
from typing import List
from pymemcache.client.base import Client
from domain.entities import MaterialRequirement, Root


class GetRequirementDataAdapter:

    @staticmethod
    def get_material_requirement(root: Root) -> List[MaterialRequirement]:
        with Client('localhost', connect_timeout=60, timeout=15, encoding='utf-8') as client:
            key = root.root_id
            material_requirements_data = client.get(key + '_material_requirements')
            result = list()

        if material_requirements_data:
            material_requirements_data = material_requirements_data.decode('utf-8')
            material_requirements_data = json.loads(material_requirements_data)
            result = list(map(lambda item: MaterialRequirement.from_dict(item), material_requirements_data))

        return result
