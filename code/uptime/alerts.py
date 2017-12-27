import boto3
from uptime.logging import sentry_client, logger

@sentry_client.capture_exceptions
def handler(event, context):
    """
    listen to an SNS topic and send out (email) alerts.

    since we're in sandbox mode only send out emails to the developper
    """
    client = boto3.client('ses', region_name='eu-west-1')
    response = client.send_email(
        Source='noreply@uptime.rocks',
        Destination={
            'ToAddresses': [
                'hello@uptime.rocks',  # TODO: move SES account out of sandbox and use the real recipient here
            ],
        },
        Message={
            'Subject': {
                'Data': 'uptime.rocks: Alert!',
                'Charset': 'utf8'
            },
            'Body': {
                'Text': {
                    'Data': str(event),
                    'Charset': 'utf8'
                }
            }
        },
        #ReplyToAddresses=[
        #    replyTo
        #]
    )
    return { 'messageId': response['MessageId'] }