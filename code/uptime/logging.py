import logging
import local_secrets
from raven.contrib.awslambda import LambdaClient

# provide some defaults to the other modules
logger = logging.getLogger()
logger.setLevel(logging.INFO)
sentry_client = LambdaClient(local_secrets.SENTRY_DSN)