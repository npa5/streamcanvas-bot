import log21

logger = log21.get_logger('logger')

def info(msg):
    logger.info(msg)

def warn(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)