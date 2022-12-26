import json
import logging
from typing import List
from pymemcache.client.base import Client
from domain.entities import MaterialSupply, Root


class CacheRequirementDataAdapter:

    @staticmethod
    def _get_memcached_client():
        client = Client('localhost', connect_timeout=60, timeout=15, encoding='utf-8')
        try:
            client.stats()
            return client
        except:
            logging.warning('Memcached server is not running')
            client.close()
            return None

    @staticmethod
    def _get_key_value(data: dict, main_root_id: str):
        key = main_root_id + '_material_supply_' + data['root_id'] + '_' + data['code']
        value = json.dumps(data)
        return key, value

    @classmethod
    def execute(cls, main_root: Root, items: List[MaterialSupply]):
        client = cls._get_memcached_client()
        if client:
            material_supplies = list(map(lambda x: x.to_dict(), items))
            cached_data = dict(map(lambda x: cls._get_key_value(x, main_root.root_id), material_supplies))
            root_key = main_root.root_id + '_material_supply'
            cached_data_keys = json.dumps(list(cached_data.keys()))
            index = 0
            total = len(cached_data_keys)
            counter = 0
            cached_data_keys_dict = {root_key: total}

            part_size = 1000000
            while counter < total:

                take = part_size + counter if total - counter >= part_size else total
                cached_data_keys_dict[f'{root_key}_{index}'] = cached_data_keys[counter:take]
                index += 1
                counter = take

            cached_data.update(cached_data_keys_dict)

            status = client.set_many(cached_data, expire=79200)
            client.close()
