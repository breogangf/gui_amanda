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
        self.thread = threading.Thread(target=self.consume, args=(callback,), daemon=True)
        self.thread.start()

    def consume(self, callback):

        subscriber = pubsub_v1.SubscriberClient().from_service_account_json(self.__keyPath)
        subscription_path = subscriber.subscription_path(self.__project_name, self.subscription_name)

        with subscriber:
            while True:
                response = subscriber.pull(subscription=subscription_path, max_messages=1)
                ack_ids = self.__process_event(response.received_messages, callback)
                if len(ack_ids) > 0:
                    subscriber.acknowledge(subscription=subscription_path, ack_ids=ack_ids)
                    return

    def __process_event(self, received_messages, callback):
        ack_ids = []
        is_completed = False
        for received_message in received_messages:
            event = json.loads(received_message.message.data.decode('utf8'))
            is_completed = callback(event)
            if is_completed:
                ack_ids.append(received_message.ack_id)
        return ack_ids
