import logging
import sys

from plone.registry.interfaces import IRegistry
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IRedirectAfterLogin
from Products.CMFPlone.PloneBaseTool import getExprContext
from zope.component import getUtility
from zope.interface import implementer
from zope.site.hooks import getSite


logger = logging.getLogger('collective.onlogin')
outahere = 'audi5000'
settings = 'collective.onlogin.interfaces.IOnloginSettings.'
redirect_enabled = settings+'login_redirect_enabled' 
first_enabled    = settings+'first_login_redirect_enabled'
ignore_redirect  = settings+'login_redirect_ignore_came_from'
ignore_first     = settings+'first_login_redirect_ignore_came_from'
redirect_expr    = settings+'login_redirect_expr'
first_expr       = settings+'first_login_redirect_expr'



def logException(msg, context=None):
    logger.exception(msg)
    if context is not None:
        error_log = getattr(context, 'error_log', None)
        if error_log is not None:
            error_log.raising(sys.exc_info())

@implementer(IRedirectAfterLogin)
class RedirectAfterLoginAdapter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.came_from = self.request.get('came_from')
        registry = getUtility(IRegistry)
        # check if we need to redirect at all
        self.do_redirect            = registry.get(redirect_enabled)
        # check if we need to ignore came_from variable
        self.ignore_came_from       = registry.get(ignore_redirect)
        # check if we got redirect expression
        self.redirect_expr          = registry.get(redirect_expr)
        # check if we need to redirect on first login at all
        self.do_redirect_first      = registry.get(first_enabled)
        # check if we need to ignore came_from variable on first login
        self.ignore_came_from_first = registry.get(ignore_first)
        # check if we got redirect expression for first login
        self.redirect_expr_first    = registry.get(first_expr)


    def __call__(self, came_from=None, is_first_login=False):

        if not is_first_login:
            logger.info('userlogin')
            logger.info('do_redirect {}'.format(self.do_redirect))
            if not self.do_redirect:
                logger.info(outahere)
                return

            logger.info('ignore_came_from {}'.format(self.ignore_came_from))
            logger.info('came_from ' + self.came_from)
            if not self.ignore_came_from and self.came_from:
                logger.info(outahere)
                return self.came_from

            actual_redirect_expr = self.redirect_expr
            
        else:
            logger.info('initial login')
            logger.info('do_redirect_first {}'.format(self.do_redirect_first))
            if not self.do_redirect_first:
                logger.info(outahere)
                return
            
            ignore = self.ignore_came_from_first
            logger.info('ignore_came_from_first {}'.format(ignore))
            logger.info('came_from ' + self.came_from)
            if not self.ignore_came_from_first and self.came_from:
                logger.info(outahere)
                return self.came_from

            actual_redirect_expr = self.redirect_expr_first

        logger.info('redirect_expr ' + actual_redirect_expr)
        if not actual_redirect_expr:
            logger.info(outahere)
            return


        # check if we have access to the request object
        logger.info('request {}'.format(len(self.request)))
        if not self.request:
            logger.info(outahere)
            return

        # get portal object
        portal = getSite()
            
        # now complile and render our expression to url
        expr = Expression(actual_redirect_expr)
        econtext = getExprContext(portal, portal)
        try:
            url = expr(econtext)
        except Exception:
            logException(u'Error during user login redirect')
            return
        else:
            # check if came_from is not empty, then clear it up, otherwise 
            # further Plone scripts will override our redirect
            if self.request.get('came_from'):
                self.request['came_from'] = ''
                self.request.form['came_from'] = ''
            logger.info('redirecting to: {}'.format(url))
            
        return url


