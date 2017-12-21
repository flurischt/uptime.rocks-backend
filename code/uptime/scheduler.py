import json
import os
import time
import boto3

from boto3.dynamodb.conditions import Attr
from uptime.logging import sentry_client, logger

# dynamodb prototype
status_table = boto3.resource('dynamodb').Table(os.getenv('TABLE_NAME'))

lambdas = boto3.client('lambda')
worker_name = os.getenv('WORKER_LAMBDA_NAME')

UPDATE_INTERVAL_IN_SEC = 5 * 60

@sentry_client.capture_exceptions
def handler(event, context):
    logger.info('scheduler.handler got event {}'.format(event))
    # get all services that have not been checked in the last UPDATE_INTERVAL_IN_SEC seconds
    last_check_time = int(time.time()) - UPDATE_INTERVAL_IN_SEC
    response = status_table.scan(
        ProjectionExpression='id',
        FilterExpression = Attr('last_check').lt(last_check_time)
    )
    logger.info('Found {} services to be checked.'.format(response['Count']))
    # and let the workers process them
    for item in response['Items']:
        logger.info('asynchronously invoking lambda: {} for id={}'.format(worker_name, item['id']))
        lambdas.invoke(
            FunctionName = worker_name,
            InvocationType = 'Event',
            Payload = json.dumps(item),
        )

    return json.dumps({
        'num_enqueued': response['Count']
    })