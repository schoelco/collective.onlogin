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
from Products.CMFPlone.interfaces import IRedirectAfterLogin
from Products.CMFPlone.PloneBaseTool import getExprContext
from zope.component import getUtility
from zope.interface import implementer


def OUTAHERE():
    logger.info('audi5000')


@implementer(IRedirectAfterLogin)
class RedirectAfterLoginAdapter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.came_from = self.request.get('came_from')
        registry = getUtility(IRegistry)
        # check if we need to redirect at all
        self.do_redirect = registry.get(REDIRECT_ENABLED)
        # check if we need to ignore came_from variable
        self.ignore_came_from = registry.get(IGNORE_REDIRECT)
        # check if we got redirect expression
        self.redirect_expr = registry.get(REDIRECT_EXPR)
        # check if we need to redirect on first login at all
        self.do_redirect_first = registry.get(FIRST_ENABLED)
        # check if we need to ignore came_from variable on first login
        self.ignore_came_from_first = registry.get(IGNORE_FIRST)
        # check if we got redirect expression for first login
        self.redirect_expr_first = registry.get(FIRST_EXPR)

    def __call__(self, came_from=None, is_first_login=False):

        if not is_first_login:
            logger.info('userlogin')
            logger.info('do_redirect {0}'.format(self.do_redirect))
            if not self.do_redirect:
                OUTAHERE()
                return

            logger.info('ignore_came_from {0}'.format(self.ignore_came_from))
            logger.info('came_from ' + self.came_from)
            if not self.ignore_came_from and self.came_from:
                OUTAHERE()
                return self.came_from

            actual_redirect_expr = self.redirect_expr

        else:
            logger.info('initial login')
            logger.info('do_redirect_first {0}'.format(self.do_redirect_first))
            if not self.do_redirect_first:
                OUTAHERE()
                return

            ignore = self.ignore_came_from_first
            logger.info('ignore_came_from_first {0}'.format(ignore))
            logger.info('came_from ' + self.came_from)
            if not self.ignore_came_from_first and self.came_from:
                OUTAHERE()
                return self.came_from

            actual_redirect_expr = self.redirect_expr_first

        logger.info('redirect_expr ' + actual_redirect_expr)
        if not actual_redirect_expr:
            OUTAHERE()
            return

        # check if we have access to the request object
        logger.info('request {0}'.format(len(self.request)))
        if not self.request:
            OUTAHERE()
            return

        # get portal object
        portal = get_portal()

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
            logger.info('redirecting to: ' + url)

        return url
