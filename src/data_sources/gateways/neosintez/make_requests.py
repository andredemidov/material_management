import asyncio
from typing import Literal
from .init_one_request_coroutine import InitOneRequestCoroutine

METHODS = Literal['get', 'post', 'delete', 'put']


class MakeRequests:

    @classmethod
    def execute(cls, payloads: list[dict], session, method: METHODS = 'get', pool_size: int = 20) -> list[dict]:
        """Метод выполняет запрос в неосинтез.
        Принимает аргументы: payloads: list[dict] - каждый dict должен содержать
        ключи route и request_body, session - объект aiohttp.ClientSession(), method: str - по умолчанию get,
        pool_size: int - по умолчанию 20 - это количество запросов, которые будут отправлены асинхронно.
        Возвращает список dict с ключами status и data"""
        prepared_payloads = cls._prepare_payloads(payloads, session, pool_size)
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(cls._get_coroutine(prepared_payloads, session, method))
        return result

    @classmethod
    def _get_tasks(cls, payloads: list[dict], session, method):
        tasks = list()
        for payload in payloads:
            tasks.append(asyncio.create_task(InitOneRequestCoroutine.execute(
                session,
                payload['route'],
                payload['request_body'],
                method
            )))
        return tasks

    @staticmethod
    def _pool_payloads(items: list, step: int):
        result = list()
        counter = 0
        total = len(items)
        while counter < total:
            take = total - counter if total - counter <= step else step
            pool = items[counter:take + counter]
            result.append(pool)
            counter += take
        return result

    @classmethod
    def _prepare_payloads(cls, payloads, session, pool_size):
        return cls._pool_payloads(payloads, pool_size)

    @classmethod
    async def _get_coroutine(cls, prepared_payloads: list[list], session, method: METHODS) -> list[dict]:
        result = list()
        print(f'total payloads pool {len(prepared_payloads)}')
        counter = 0
        for payload in prepared_payloads:
            counter += 1
            print(f'{counter} start pool')
            tasks = cls._get_tasks(payload, session, method)
            responses = await asyncio.gather(*tasks)
            print('responses are got')
            result.extend(responses)
        return result
