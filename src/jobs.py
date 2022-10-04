import os
import json
import time

from .setup_logger import logger
from src.authentication import Authencation
from src.listener import Listener

class Jobs(Authencation):

    __subscription_jobs = os.environ.get('SUBSCRIPTION_JOBS')

    def __init__(self, workflow_id):
        super().__init__()
        self.workflow_id = workflow_id
        self.job_id = None
        self.status = None
        self.job_completed = False
        self.data = {}
        self.listener = Listener(self.__subscription_jobs, self.__mark_as_completed)

    def process(self, processed_callback, assets = []):
        self.processed_callback = processed_callback
        asset_ids = list(map(lambda asset: asset.asset_id, assets))
        body = self.__build_job_body(asset_ids)
        created_job = self.do_authentication_request('POST', '/jobs', json=body)
        self.job_id = created_job['jobId']
        self.status = created_job['status']['job']
        self.data = created_job
        logger.info(f'Created job by jobId "{self.job_id}"')
        return created_job

    def read(self):
        return self.do_authentication_request('GET', f'/jobs/{self.job_id}')

    def __mark_as_completed(self, event):
        if self.job_id == event['jobId']:
            self.status = event['status']['job']
            self.job_completed = True if self.status == 'finished' or self.status == 'failed' else False
            if self.job_completed:
                self.data = event
                self.processed_callback()
                logger.info(f'Job {event["jobId"]} marks as completed')
        return self.job_completed

    def is_completed(self):
        return self.job_completed

    def start_polling(self):
        logger.info(f'Checking "{self.job_id}" is processed...')

        while self.status == 'created' or self.status == 'in progress':
            time.sleep(2)
            processing_job = self.read()
            self.status = processing_job['status']['job']

        logger.info(f'JobId "{self.job_id}" processed')
        self.data = processing_job
        return processing_job

    def get_delivery_urls(self):
        if self.status == 'finished':
            results = self.data['assets']['outputs']['result']
            urls = list(map(lambda result: result['url'], results))
            return urls
        return []

    def __build_job_body(self, asset_ids):
        return {
            "workflow": {
                "id": self.workflow_id
            },
            "assets": {
                "inputs": asset_ids,
                "outputs": {
                    "visibility": "PUBLIC"
                }
            }
        }

    def __str__(self):
        return json.dumps(self.data, indent=3)
