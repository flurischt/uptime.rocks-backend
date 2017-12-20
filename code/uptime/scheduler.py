import json
import os
import boto3
from uptime.logging import sentry_client, logger

# dynamodb prototype
status_table = boto3.resource('dynamodb').Table(os.getenv('TABLE_NAME'))

@sentry_client.capture_exceptions
def handler(event, context):
    logger.info('scheduler.handler got event {}'.format(event))
    # # let's try out dynamodb
    # from random import randint
    # import time
    # for _ in range(100):
    #     id = str(randint(0, 10000))
    #     status_table.put_item(
    #         Item={
    #             'id': id,
    #             'last_check': int(time.time()),
    #             'label': 'label nr. {}'.format(id),
    #             'whatever': 'bli bla blu',
    #         }
    #     )

    # async invoke the worker
    client = boto3.client('lambda')
    worker = os.environ['WORKER_LAMBDA_NAME']
    logger.info('asynchronously invoking lambda: {}'.format(worker))
    client.invoke(
        FunctionName = worker,
        InvocationType = 'Event',
        Payload = json.dumps(
            {
                'reason': 'test'
            }
        ),
    )
    return 'Success?'