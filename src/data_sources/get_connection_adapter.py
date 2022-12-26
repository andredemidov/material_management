from .gateways.neosintez import GetSession


class GetConnectionAdapter:

    def __init__(self, url):
        self._url = url

    @staticmethod
    def _get_auth_string(authentication_config: dict):
        auth_data = [
            f"grant_type={authentication_config['grant_type']}",
            f"username={authentication_config['username']}",
            f"password={authentication_config['password']}",
            f"client_id={authentication_config['client_id']}",
            f"client_secret={authentication_config['client_secret']}",
        ]
        auth_string = '&'.join(auth_data)
        return auth_string

    def execute(self, authentication_config):
        """Метод принимает dict authentication_config с ключами grant_type,
        username, password, client_id, client_secret. Возвращает объект сессии"""
        auth_string = self._get_auth_string(authentication_config)
        session = GetSession.execute(self._url, auth_string)
        return session
