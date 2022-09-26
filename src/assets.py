import os
import mimetypes
import json
import requests
import time

from .setup_logger import logger
from src.authentication import Authencation

class Assets(Authencation):

    def __init__(self, path):
        super().__init__()
        self.asset_id = None
        self.asset_completed = False
        self.asset_data = {}
        self.path =  path
        self.tenant = 'Zara'
        self.visibility = 'PUBLIC'
        self.__set_information(path)
        logger.info(f'New asset instance by name "{self.asset_name}"')


    def upload(self):
        data = self.__get_signed_url()
        logger.info(f'Obtained a signed url by asset name "{self.asset_name}"')

        self.asset_id = data['assetId']
        self.__upload_asset(data['url'])
        logger.info(f'Uploaded asset name "{self.asset_name}" with assetId "{self.asset_id}"')

        logger.info(f'Checking "{self.asset_id}" is completed...')
        self.__start_polling()
        logger.info(f'AssetId "{self.asset_id}" completed')

        return self.asset_id

    def read(self):
        return self.do_authentication_request('GET', f'/assets/{self.asset_id}')

    def is_completed(self):
        return self.asset_completed

    def __get_signed_url(self):
        headers = {'Content-Type': 'application/json'}
        body = self.__build_body_asset()
        fetch_url = self.buildUrl('/signedUrl')
        response_signed_url = requests.post(fetch_url, headers=headers, json=body, verify=False)
        return response_signed_url.json()

    def __upload_asset(self, signedUrl):
        asset_stream = open(self.path, 'rb')
        google_headers = self.__get_google_headers()
        requests.put(signedUrl, headers=google_headers, data=asset_stream, verify=False)

    def __start_polling(self):
        while not self.is_completed():
            time.sleep(1)
            self.asset_data = self.read()
            self.asset_completed = True if 'deliveryURL' in self.asset_data['metadata'] else False

    def __set_information(self, path):
        self.asset_name = os.path.basename(path)
        self.content_type = mimetypes.MimeTypes().guess_type(self.asset_name)[0]
        self.content_length = os.path.getsize(path)

    def __get_service_account(self):
        authenticated_session = self.get_authentication_session()
        return authenticated_session.credentials.service_account_email

    def __build_body_asset(self):
        return {
            'optimize': False,
            'metadata': {
                'partnumber': 'xxx',
                'brand': self.tenant,
                'application': 'xxx'
            },
            'contentType': self.content_type,
            'contentLength': self.content_length,
            'originalAssetName': self.asset_name,
            'serviceAccount': self.__get_service_account(),
            'visibility': self.visibility,
            'tenant': self.tenant
        }

    def __get_google_headers(self):
        return {
            'Content-Type': self.content_type,
            'x-goog-content-length-range': f'{self.content_length},{self.content_length}',
            'x-goog-meta-sa': self.__get_service_account(),
            'x-goog-meta-assetid': self.asset_id,
            'x-goog-meta-originalassetname': self.asset_name,
            'x-goog-meta-tenant': self.tenant,
            'x-goog-meta-visibility': self.visibility,
        }

    def __str__(self):
        return json.dumps(self.data, indent=3)