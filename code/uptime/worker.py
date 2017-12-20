from uptime.logging import sentry_client, logger

@sentry_client.capture_exceptions
def handler(event, context):
    logger.info('worker.handler started for service-id: {}'.format(event['id']))
    # TODO: check the service and update status table
    return 'Success'