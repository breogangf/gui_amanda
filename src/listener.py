import os
import json
import threading
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.types import FlowControl
from .setup_logger import logger

flow_control_settings = FlowControl(max_messages=1)

class Listener:

    __keyPath = os.environ.get('KEY_PATH')
    __project_name = os.environ.get('PROJECT_NAME')

    def __init__(self, subscription_name, callback):
        self.subscription_name = subscription_name
        self.callback = callback
        self.thread = threading.Thread(target=self.__create_subscriber)
        self.thread.start()

    def __create_subscriber(self):
        subscriber = pubsub_v1.SubscriberClient().from_service_account_json(self.__keyPath)
        subscription_path = subscriber.subscription_path(self.__project_name, self.subscription_name)
        streaming_pull_future = subscriber.subscribe(subscription_path, self.__receiveEvent, flow_control=flow_control_settings)
        logger.info(f'Created subscriber for {subscription_path}')
        with subscriber:
            try:
                streaming_pull_future.result()
            except Exception:
                streaming_pull_future.cancel()  # Trigger the shutdown.
                streaming_pull_future.result()  # Block until the shutdown is complete.

    def __receiveEvent(self, message):
        event = json.loads(str(message.data, 'utf8'))
        is_completed = self.callback(event)
        if is_completed:
            message.ack()
            self.thread.join()
        else:
            message.nack()
