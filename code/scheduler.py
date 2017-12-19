import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info('scheduler.handler got event {}'.format(event))
    client = boto3.client('lambda')
    worker = os.environ['WORKER_LAMBDA_NAME']
    logger.info('asynchronously invoking lambda: {}'.format(worker))
    client.invoke(
        FunctionName = worker,
        InvocationType = 'Event',
        Payload = b"{'name': 'test'}",
    )
    return 'Success?'