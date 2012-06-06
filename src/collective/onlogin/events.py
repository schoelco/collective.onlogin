import sys
import logging

from zope.component import getUtility
from zope.site.hooks import getSite

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFPlone.PloneBaseTool import getExprContext
from Products.PlonePAS.interfaces.events import IUserInitialLoginInEvent

from plone.registry.interfaces import IRegistry

logger = logging.getLogger('collective.onlogin')
def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())

def userLogin(obj, event):
    """Redirects logged in users to personal dashboard"""
    # get registry where we keep our configuration
    registry = getUtility(IRegistry)

    # check if we need to redirect at all
    do_redirect = registry.get(
        'collective.onlogin.interfaces.IOnloginSettings.login_redirect_enabled')
    if not do_redirect:
        return

    # do not redirect if user initial login is set and our current event
    # is about User Initial Login; so First Login Redirect is always of
    # higher priority
    if registry.get('collective.onlogin.interfaces.IOnloginSettings.' \
       'first_login_redirect_enabled') and \
       IUserInitialLoginInEvent.providedBy(event):
        return

    # get portal object
    portal = getSite()
        
    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return

    # check if we need to ignore came_from variable
    ignore_came_from = registry.get(
        'collective.onlogin.interfaces.IOnloginSettings.' \
        'login_redirect_ignore_came_from')
    # when we try to log from logged_out page the came_from doesn't bin canceled
    if not ignore_came_from and request.get('came_from'):
        return

    # check if we got redirect expression
    redirect_expr = registry.get(
         'collective.onlogin.interfaces.IOnloginSettings.login_redirect_expr')
    if not redirect_expr:
        return

    # now complile and render our expression to url
    expr = Expression(redirect_expr)
    econtext = getExprContext(portal, portal)
    try:
        url = expr(econtext)
    except Exception, e:
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

    # check if we need to redirect at all
    do_redirect = registry.get('collective.onlogin.interfaces.' \
        'IOnloginSettings.first_login_redirect_enabled')
    if not do_redirect:
        return

    # get portal object
    portal = getSite()

    # check if we have an access to request object
    request = getattr(portal, 'REQUEST', None)
    if not request:
        return

    # check if we need to ignore came_from variable
    ignore_came_from = registry.get(
        'collective.onlogin.interfaces.IOnloginSettings.' \
        'first_login_redirect_ignore_came_from')
    # when we try to log from logged_out page the came_from doesn't bin canceled
    if not ignore_came_from and request.get('came_from'):
        return

    # check if we got redirect expression
    redirect_expr = registry.get('collective.onlogin.interfaces.' \
        'IOnloginSettings.first_login_redirect_expr')

    if not redirect_expr:
        return

    # now complile and render our expression to url
    expr = Expression(redirect_expr)
    econtext = getExprContext(portal, portal)
    try:
        url = expr(econtext)
    except Exception, e:
        logException(u'Error during user initial login redirect')
        return
    else:
        # check if came_from is not empty, then clear it up, otherwise further
        # Plone scripts will override our redirect
        if request.get('came_from'):
            request['came_from'] = ''
            request.form['came_from'] = ''
        request.RESPONSE.redirect(url)
