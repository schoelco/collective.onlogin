import logging
import sys


logger = logging.getLogger('collective.onlogin')

def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
