from uptime.logging import sentry_client

@sentry_client.capture_exceptions
def handler(event, context):
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {}, #{ 'headerName': 'headerValue', ... },
        'body': 'Success from the ping handler'
    }
