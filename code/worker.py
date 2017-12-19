import logging
import local_secrets
from raven.contrib.awslambda import LambdaClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = LambdaClient(local_secrets.SENTRY_DSN)

@client.capture_exceptions
def handler(event, context):
    logger.info('worker.handler got event {}'.format(event))
    return 'Success'