import json


class InitOneRequestCoroutine:

    @staticmethod
    async def execute(session, route, request_body, method) -> dict:
        payload = json.dumps(request_body)
        if 'search' in route:
            response = await session.request(method, route, data=payload, headers={'X-HTTP-Method-Override': 'GET'})
        else:
            response = await session.request(method, route, data=payload)
        async with response:
            text = await response.text()
            data = json.loads(text) if text else ''
        response.close()
        return {'status': response.status, 'data': data}
