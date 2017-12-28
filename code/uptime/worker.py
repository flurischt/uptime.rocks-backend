import os
import json

import boto3
import requests

from requests.exceptions import RequestException, ConnectionError
from uptime.logging import sentry_client, logger
from uptime.model import get_item, update_item

sns = boto3.client('sns')
topic = os.getenv('TOPIC_NAME')

def _send_alert(item_id, item_label, message):
    logger.info('sending alert for service-id: %s', item_id)
    sns.publish(
        TopicArn=topic,
        Message=json.dumps({
            'id': item_id,
            'label': item_label,
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
    logger.info('worker.handler started for service-id: %s', item_id)
    service_to_process = get_item(item_id)
    url = service_to_process['url']
    prev_status = service_to_process['check_status']
    label = service_to_process['label']
    status_code = 0
    try:
        response = requests.get(url, headers={
            'User-Agent': 'UptimeCheck/0.1 (https://uptime.rocks)'
        })
        status_code = response.status_code
        logger.info('service-id %s: http-check resulted in status-code: %s', item_id, status_code)
    except ConnectionError:
        pass  # cannot connect to service. treat the service as down
    except RequestException:
        # for all other exceptions from requests treat the service as down but log the exception
        sentry_client.captureException()
    # TODO: implement some more involved checks
    if status_code == 200:
        update_item(service_to_process)
        if prev_status != 'success':
            _send_alert(item_id, label, 'service has recovered!')
    else:
        update_item(service_to_process, success=False)
        if prev_status == 'success':
            _send_alert(item_id, label, 'service is down!')
    return 'Finished'
