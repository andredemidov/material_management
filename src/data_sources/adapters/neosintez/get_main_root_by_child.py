from domain.entities import Root
from .abstract_adapter import AbstractAdapter
from data_sources.gateways.neosintez import MakeRequests


class GetMainRootByChild(AbstractAdapter):

    def __init__(self, session):
        super().__init__(session)

    def execute(self, child_root: Root) -> Root:

        payloads = [
            {
                'route': f'/api/objects/{child_root.root_id}/path',
                'request_body': '',
            }
        ]
        results = MakeRequests.execute(payloads, self._session, 'get')
        for result in results:
            if result['status'] != 200:
                message = f"request have status not equal 200. {result['data']}"
                raise RuntimeError(message)
        path = results[0]['data']['AncestorsOrSelf']
        parent = list(filter(lambda x: x['Entity']['Id'] == self.main_root_class_id, path))
        if not parent:
            message = f"There is not parent for {child_root.root_id} with class {self.main_root_class_id}"
            raise RuntimeError(message)
        parent_id = parent[0]['Id']
        name = parent[0]['Name']

        return Root(name=name, root_id=parent_id)
