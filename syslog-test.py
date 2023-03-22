import logging
import logging.handlers

logger = logging.getLogger()
logger.setLevel(logging.INFO)
# Set the facility to local7 (23)
facility = logging.handlers.SysLogHandler.LOG_LOCAL7

handler = logging.handlers.SysLogHandler(
    address=('0.0.0.0', 514), facility=facility)
logger.addHandler(handler)

logger.error('Test syslog message')
