import requests

from requests.exceptions import RequestException
from uptime.logging import sentry_client, logger
from uptime.model import get_item, update_item

@sentry_client.capture_exceptions
def handler(event, context):
    """
    checks the service identified by 'id' 
    
    for now a simple http-status_code == 200 check is implemented.
    """
    id = event['id']
    logger.info('worker.handler started for service-id: {}'.format(id))
    service_to_process = get_item(id)
    url = service_to_process['url']
    try:
        response = requests.get(url)
        status_code = response.status_code
        logger.info('service-id {}: http-check resulted in status-code: {}'.format(id, status_code))
    except RequestException:
        sentry_client.captureException()
    # TODO: implement some more involved checks
    if status_code == 200:
        update_item(service_to_process)
    else:
        # TODO: set status to ERROR and send a notification
        logger.info('service-id {}: service seems to be down!'.format(id))
        update_item(service_to_process, success=False)
    return 'Finished'