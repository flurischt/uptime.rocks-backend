import uuid
import time
import os
import boto3
from boto3.dynamodb.conditions import Attr


SCHEMA = {
    'id': '',
    'schema_version': 1,
    'label': '',
    'url': '',
    'check_status': 'success',
    'last_check': 0,
    'next_check': 0,
    'check_interval': '15m',
}

CHECK_INTERVALS_IN_SEC = {
    '1m': 60,
    '5m': 5 * 60,
    '15m': 15 * 60,
    '1h': 60 * 60
}

status_table = boto3.resource('dynamodb').Table(os.getenv('TABLE_NAME'))


def _update_next_check(item):
    """
    helper function to update the next_check attribute.
    """
    assert item['check_interval'] in CHECK_INTERVALS_IN_SEC
    item['next_check'] = item['last_check'] + CHECK_INTERVALS_IN_SEC[item['check_interval']]


def get_item(item_id):
    """
    read all attributes for an item identified by item_id
    """
    result = status_table.get_item(
        Key={'id': item_id}
    )
    return result['Item']

def put_item(**kwargs): 
    """
    create an item in DynamoDB using uptime.model.SCHEMA and return its id.

    pass keyword-arguments to the function to set the attributes. default entries for `id` and `last_check` will be set if not given.
    """
    new_item = SCHEMA.copy()
    for key, value in kwargs.items():
        if key not in new_item.keys():
            raise Exception('SCHEMA does not support attribute {}'.format(key))
        new_item[key] = value
    if 'id' not in kwargs.keys():
        new_item['id'] = str(uuid.uuid4())
    if 'last_check' not in kwargs.keys():
        new_item['last_check'] = int(time.time())
    _update_next_check(new_item) # TODO: business logic in here?
    status_table.put_item(
        Item=new_item
    )
    return new_item['id']


def update_item(item, success=True):
    """
    puts the given item to dynamodb and updates the last_check attribute to NOW.
    """
    # since we'll use PUT make sure that the caller has provided all attributes
    # if an attribute is missing then this would be deleted from the database
    # TODO: needs a fix for schema-updates
    schema_keys_not_written = SCHEMA.keys() - item.keys()
    if len(schema_keys_not_written) > 0:
        raise Exception("update_item() called without providing all necessary SCHEMA-attributes!")
    item['last_check'] = int(time.time())
    if success:
        item['check_status'] = 'success'
    else:
        item['check_status'] = 'error'
    put_item(**item)


def scan_for_services_to_check():
    """
    yields items in DynamoDB with next_check < CURRENT_TIME
    """
    current_time = int(time.time())
    response = status_table.scan(
        ProjectionExpression='id, check_status',
        FilterExpression=Attr('next_check').lte(current_time)
    )
    # handle pagination
    while 'LastEvaluatedKey' in response.keys():
        last_key = response['LastEvaluatedKey']
        for item in response['Items']:
            yield item
        response = status_table.scan(
            ProjectionExpression='id, check_status',
            ExclusiveStartKey=last_key,
            FilterExpression=Attr('next_check').lte(current_time)
        )
    # and yield the remaining elements
    for item in response['Items']:
        yield item
    