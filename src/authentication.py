import os
import urllib3

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from dotenv import load_dotenv

load_dotenv()

class Authencation:

    __hostname = os.environ.get('HOSTNAME')
    __targetAudience = os.environ.get('TARGET_AUDIENCE')
    __keyPath = os.environ.get('KEY_PATH')

    def __init__(self):
        urllib3.disable_warnings()
        credentials = service_account.IDTokenCredentials.from_service_account_file(self.__keyPath, target_audience=self.__targetAudience)
        self.authenticated_session = AuthorizedSession(credentials)

    def get_authentication_session(self):
        return self.authenticated_session

    def do_authentication_request(self, method, path, **kwargs):
        url = self.buildUrl(path)
        response = self.authenticated_session.request(method, url, verify=False, **kwargs)
        return response.json()

    def buildUrl(self, path):
        return f'{self.__hostname}{path}'
