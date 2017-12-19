
def handler(event, context):
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {}, #{ 'headerName': 'headerValue', ... },
        'body': 'Success from the ping handler'
    }