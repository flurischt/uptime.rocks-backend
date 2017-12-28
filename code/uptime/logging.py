import logging
import local_secrets
from raven import Client
from raven.transport.http import HTTPTransport

# provide some defaults to the other modules
logger = logging.getLogger()
logger.setLevel(logging.INFO)
sentry_client = Client(dsn=local_secrets.SENTRY_DSN, transport=HTTPTransport)
