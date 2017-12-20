import json
import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# dynamodb prototype
status_table = boto3.resource('dynamodb').Table(os.getenv('TABLE_NAME'))


def handler(event, context):
    logger.info('scheduler.handler got event {}'.format(event))
    # let's try out dynamodb
    from random import randint
    status_table.put_item(
        Item={
            'id': str(randint(0, 10000)),
            'username': 'janedoe',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'age': 25,
            'account_type': 'standard_user',
        }
    )

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