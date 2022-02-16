import logging
import os

LEDGER = os.environ.setdefault('LEDGER', 'schema')
TABLE = os.environ.setdefault('TABLE', 'version_control')

LOG_LEVEL = os.environ.setdefault('LOG_LEVEL', 'NOTSET')


def get_log_level():
    """Return the current **LOG_LEVEL** in the settings as a string.

    :return: The log level
    :rtype: str
    """
    if LOG_LEVEL == 'INFO':
        return logging.INFO
    if LOG_LEVEL == 'DEBUG':
        return logging.DEBUG
    if LOG_LEVEL == 'ERROR':
        return logging.ERROR
    return logging.NOTSET
