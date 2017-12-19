import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info('worker.handler got event {}'.format(event))
    return 'Success'