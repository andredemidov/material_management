from .make_requests import MakeRequests
from .get_total import GetTotal


class MakeSearchRequests(MakeRequests):

    @classmethod
    def _split_payloads(cls, request_body, session) -> list[dict]:
        total = GetTotal.execute(request_body, session)
        counter = 0
        step = 500
        payloads = list()
        while counter < total:
            take = total - counter if total - counter <= step else step
            route = f'/api/objects/search?take={take}&skip={counter}'
            payloads.append(
                {
                    'route': route,
                    'request_body': request_body,
                }
            )
            counter += take
        return payloads

    @classmethod
    def _prepare_payloads(cls, payloads, session, pool_size):
        request_body = payloads[0]['request_body']
        splited_payloads = cls._split_payloads(request_body, session)
        return cls._pool_payloads(splited_payloads, pool_size)
