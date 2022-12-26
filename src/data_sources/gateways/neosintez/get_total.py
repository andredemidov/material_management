import asyncio
from .init_one_request_coroutine import InitOneRequestCoroutine


class GetTotal:

    @classmethod
    async def _get_total(cls, request_body, session):
        route = '/api/objects/search?take=0&skip=0'
        count_response = await InitOneRequestCoroutine.execute(session, route, request_body, 'post')
        total = count_response['data']['Total']
        print(f'total {total}')
        return total

    @classmethod
    def execute(cls, request_body, session) -> int:
        """Метод выполняет запрос в неосинтез.
                Принимает аргументы: request_body, session - объект aiohttp.ClientSession(),
                Возвращает список dict с ключами status и data"""
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(cls._get_total(request_body, session))
        return result
