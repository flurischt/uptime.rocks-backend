from uptime.logging import sentry_client, logger

@sentry_client.capture_exceptions
def handler(event, context):
    logger.info('worker.handler got event {}'.format(event))
    return 'Success'