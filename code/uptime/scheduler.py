import json
import os
import boto3
from uptime.logging import sentry_client, logger
from uptime.model import scan_for_services_to_check

lambdas = boto3.client('lambda')
worker_name = os.getenv('WORKER_LAMBDA_NAME')

@sentry_client.capture_exceptions
def handler(event, context):
    logger.info('scheduler.handler got event %s', event)
    # and let the workers process them
    count = 0
    for service in scan_for_services_to_check():
        logger.info('asynchronously invoking lambda: %s for id=%s', worker_name, service['id'])
        lambdas.invoke(
            FunctionName=worker_name,
            InvocationType='Event',
            Payload=json.dumps(service),
        )
        count += 1
    logger.info('Enqueued %s services to be checked', count)
    return json.dumps({
        'num_enqueued': count
    })
