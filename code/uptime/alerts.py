import json
import boto3
from uptime.logging import sentry_client, logger

@sentry_client.capture_exceptions
def handler(event, context):
    """
    listen to an SNS topic and send out (email) alerts.

    since we're in sandbox mode only send out emails to the developer
    """
    client = boto3.client('ses', region_name='eu-west-1')
    # TODO: should we clean this up before sending out? (xss etc?)
    payload = json.loads(event['Records'][0]['Sns']['Message'])
    response = client.send_email(
        Source='noreply@uptime.rocks',
        Destination={
            'ToAddresses': [
                'hello@uptime.rocks',  # TODO: move SES account out of sandbox and use the real recipient here
            ],
        },
        Message={
            'Subject': {
                'Data': 'uptime.rocks alert for service {}: {}'.format(payload['label'], payload['message']),
                'Charset': 'utf8'
            },
            'Body': {
                'Text': {
                    'Data': 'Service-ID: {} , Label: {}'.format(payload['id'], payload['label']),
                    'Charset': 'utf8'
                }
            }
        },
        #ReplyToAddresses=[
        #    replyTo
        #]
    )
    logger.info(
        'sent message regarding service-id: %s. MessageId: %s',
        payload['id'],
        response['MessageId']
    )
    return {'messageId': response['MessageId']}
