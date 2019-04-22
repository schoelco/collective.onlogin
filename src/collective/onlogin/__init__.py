# -*- coding: utf-8 -*-


import logging
import sys


logger = logging.getLogger('collective.onlogin')
SETTINGS = 'collective.onlogin.interfaces.IOnloginSettings.'
REDIRECT_ENABLED = SETTINGS+'login_redirect_enabled'
FIRST_ENABLED = SETTINGS+'first_login_redirect_enabled'
IGNORE_REDIRECT = SETTINGS+'login_redirect_ignore_came_from'
IGNORE_FIRST = SETTINGS+'first_login_redirect_ignore_came_from'
REDIRECT_EXPR = SETTINGS+'login_redirect_expr'
FIRST_EXPR = SETTINGS+'first_login_redirect_expr'


def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
