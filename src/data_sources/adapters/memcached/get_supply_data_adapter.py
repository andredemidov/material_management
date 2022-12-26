import json
import logging
from typing import List
from pymemcache.client.base import Client
from domain.entities import MaterialSupply, Root


class GetSupplyDataAdapter:

    @staticmethod
    def _get_memcached_client():
        client = Client('localhost', connect_timeout=60, timeout=15, encoding='utf-8')
        try:
            client.stats()
            return client
        except Exception as e:
            print(e)
            logging.warning('Memcached server is not running')
            client.close()
            return None

    @classmethod
    def execute(cls, main_root: Root) -> List[MaterialSupply]:
        client = cls._get_memcached_client()
        result = list()
        if client:
            root_key = main_root.root_id + '_material_supply'
            keys_len = client.get(root_key)
            if keys_len:
                keys_len = int(keys_len)
                keys = str()
                index = 0
                while len(keys) < keys_len:
                    part = client.get(f'{root_key}_{index}')
                    if not part:
                        message = f'There are no enough data in memcached for {root_key}'
                        raise ValueError(message)
                    keys += part.decode('utf-8')
                    index += 1

                keys = json.loads(keys)
                material_supplies_data = client.get_many(keys)
                client.close()
                values = material_supplies_data.values()
                result = list(map(lambda item: MaterialSupply.from_dict(json.loads(item.decode('utf-8'))), values))

        return result
