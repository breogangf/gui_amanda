from dotenv import load_dotenv
load_dotenv()

import time
from src.setup_logger import logger
from src.assets import Assets
from src.jobs import Jobs
from src.utils import get_workflow_by_name

if __name__ == '__main__':

    asset = Assets('/Users/kairos/Pictures/foto01.jpg')
    asset.upload()

    while not asset.is_completed():
        time.sleep(1)

    job = Jobs(get_workflow_by_name('amanda-wf-euw4-dev-001-image-width-resize'))
    job.process([asset])
    #job.start_polling()

    while not job.is_completed():
        time.sleep(1)

    delivery_urls = job.get_delivery_urls()
    logger.info(f'Delivery Urls by jobId "{job.job_id}":')
    [logger.info(f'\t{delivery_url}') for delivery_url in delivery_urls]