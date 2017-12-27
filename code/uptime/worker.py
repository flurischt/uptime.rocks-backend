import os
import json

import boto3
import requests

from requests.exceptions import RequestException
from uptime.logging import sentry_client, logger
from uptime.model import get_item, update_item

sns = boto3.client('sns')
topic = os.getenv('TOPIC_NAME')

def _send_alert(item_id, message):
    logger.info('sending alert for service-id: {}'.format(item_id))
    sns.publish(
        TopicArn = topic,
        Message=json.dumps({
            'id': item_id,
            'message': message 
        }),
        # we'll send json as a "string". If set to json then we would have to use 
        MessageStructure='string',
    )

@sentry_client.capture_exceptions
def handler(event, context):
    """
    checks the service identified by 'id' 
    
    for now a simple http-status_code == 200 check is implemented.
    """
    item_id = event['id']
    logger.info('worker.handler started for service-id: {}'.format(item_id))
    service_to_process = get_item(item_id)
    url = service_to_process['url']
    prev_status = service_to_process['status']
    status_code = 0
    try:
        response = requests.get(url)
        status_code = response.status_code
        logger.info('service-id {}: http-check resulted in status-code: {}'.format(item_id, status_code))
    except RequestException:
        sentry_client.captureException()
    # TODO: implement some more involved checks
    if status_code == 200:
        update_item(service_to_process)
        if prev_status <> 'success':
            _send_alert(item_id, "service has recovered!")    
    else:
        _send_alert(item_id, "service is down!")
        update_item(service_to_process, success=False)
    return 'Finished'