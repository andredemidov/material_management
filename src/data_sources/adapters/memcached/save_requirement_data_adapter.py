import json
from typing import List
from pymemcache.client.base import Client
from domain.entities import MaterialRequirement, Root


class SaveRequirementDataAdapter:

    @staticmethod
    def save_material_requirement(root: Root, data: List[MaterialRequirement]):
        material_requirements = list(map(lambda x: x.to_dict(), data))
        material_requirements = json.dumps(material_requirements)
        key = root.root_id
        with Client('localhost', connect_timeout=20, timeout=20, encoding='UTF-8') as client:
            client.set(key + '_material_requirements', material_requirements, expire=1800)
