import requests
import aiohttp
import os.path


class GetSession:

    @staticmethod
    def _get_new_token(url, auth_string):
        """
        Метод возвращает токен для аутентификации в Неосинтез на основании данных для аутентификации
        auth_string - строка вида grant_type=password&username=???&password=??&client_id=??&client_secret=??
        """
        req_url = url + '/connect/token'
        payload = auth_string
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        with requests.session() as session:
            response = session.post(req_url, data=payload, headers=headers)
            text = response.json()

        if response.status_code != 200:
            raise Exception(f'Error connect to Neosintez for url {url}')

        return text['access_token']

    @classmethod
    def _get_token(cls, url, auth_string):
        if os.path.isfile('token.txt'):
            return cls._read_token_from_file()
        else:
            return cls._get_new_token(url, auth_string)

    @staticmethod
    def _read_token_from_file() -> str:
        with open('token.txt') as f:
            token = f.read()
        return token

    @classmethod
    def execute(cls, url, auth_string):
        token = cls._get_token(url, auth_string)
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json-patch+json',
        }
        timeout = aiohttp.ClientTimeout(total=300, connect=15)
        session = aiohttp.ClientSession(url, headers=headers, timeout=timeout)
        return session
