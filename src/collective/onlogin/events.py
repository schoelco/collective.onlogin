# -*- coding: utf-8 -*-


from collective.onlogin import FIRST_ENABLED
from collective.onlogin import FIRST_EXPR
from collective.onlogin import IGNORE_FIRST
from collective.onlogin import IGNORE_REDIRECT
from collective.onlogin import logException
from collective.onlogin import logger
from collective.onlogin import REDIRECT_ENABLED
from collective.onlogin import REDIRECT_EXPR
from plone.api.portal import get as get_portal
from plone.registry.interfaces import IRegistry
from Products.CMFCore.Expression import Expression
from Products.CMFPlone.PloneBaseTool import getExprContext
from Products.PlonePAS.interfaces.events import IUserInitialLoginInEvent
from zope.component import getUtility


def OUTAHERE():
    logger.info('audi5000')


def userLogin(obj, event):
    """Redirects logged in users to personal dashboard"""
    # get registry where we keep our configuration
    registry = getUtility(IRegistry)
    logger.info('userlogin')
    # check if we need to redirect at all
    do_redirect = registry.get(REDIRECT_ENABLED)
    logger.info('do_redirect {0}'.format(do_redirect))
    if not do_redirect:
        OUTAHERE()
        return

    # do not redirect if user initial login is set and our current event
    # is about User Initial Login; so First Login Redirect is always of
    # higher priority
    if registry.get(FIRST_ENABLED) and \
       IUserInitialLoginInEvent.providedBy(event):
        OUTAHERE()
        return

    # get portal object
    portal = get_portal()

    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    logger.info('request {0}'.format(len(request)))
    if not request:
        OUTAHERE()
        return

    # check if we need to ignore came_from variable
    ignore_came_from = registry.get(IGNORE_REDIRECT)
    # when we try to log in from logged_out page the came_from isn't canceled
    if not ignore_came_from and request.get('came_from'):
        return

    # check if we got redirect expression
    redirect_expr = registry.get(REDIRECT_EXPR)
    if not redirect_expr:
        return

    # now compile and render our expression to url
    expr = Expression(redirect_expr)
    econtext = getExprContext(portal, portal)
    try:
        url = expr(econtext)
    except Exception:
        logException(u'Error during user login redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url)


def userInitialLogin(obj, event):
    """Redirects initially logged in users to getting started wizard"""
    registry = getUtility(IRegistry)

    logger.info('initial login')
    # check if we need to redirect at all
    do_redirect = registry.get(FIRST_ENABLED)

    logger.info('do_redirect {0}'.format(do_redirect))
    if not do_redirect:
        OUTAHERE()
        return

    # get portal object
    portal = get_portal()

    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)

    logger.info('request {0}'.format(len(request)))
    if not request:
        OUTAHERE()
        return

    # check if we need to ignore came_from variable
    ignore_came_from = registry.get(IGNORE_FIRST)
    # when we try to log in from logged_out page the came_from is not canceled
    logger.info('ignore_came_from {0}'.format(ignore_came_from))
    if not ignore_came_from and request.get('came_from'):
        OUTAHERE()
        return

    # check if we got redirect expression
    redirect_expr = registry.get(FIRST_EXPR)
    logger.info('redirect_expr {0}'.format(redirect_expr))
    if not redirect_expr:
        OUTAHERE()
        return

    # now complile and render our expression to url
    expr = Expression(redirect_expr)
    econtext = getExprContext(portal, portal)
    try:
        url = expr(econtext)
        logger.info('url {0}'.format(url))
    except Exception:
        logException(u'Error during user initial login redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url)
