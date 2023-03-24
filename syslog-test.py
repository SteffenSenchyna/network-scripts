import logging
import logging.handlers
import socket


def syslogMock():
    logger = logging.getLogger()
    # Set the facility to local7 (23)
    facility = logging.handlers.SysLogHandler.LOG_LOCAL7

    handler = logging.handlers.SysLogHandler(
        address=('0.0.0.0', 514))
    logger.addHandler(handler)

    logger.critical(
        "104: *Mar 22 21:29:10.128: %SYS-5-CONFIG_I: Configured from console by console")


syslogMock()
