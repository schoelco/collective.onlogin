import unittest2 as unittest

from zope.component import getUtility
from zope.interface import alsoProvides, noLongerProvides

from Products.PlonePAS.interfaces.events import IUserInitialLoginInEvent

from plone.registry.interfaces import IRegistry

from collective.onlogin.events import userLogin, userInitialLogin
from collective.onlogin.testing import COLLECTIVE_ONLOGIN_INTEGRATION_TESTING


class EventsTests(unittest.TestCase):

    layer = COLLECTIVE_ONLOGIN_INTEGRATION_TESTING
    
    def test_userLogin_disable_redirect(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # check if our function doesn't doing redirect in our case the header
        # location doesn't changed when the onlogin redirect checkbox is setting
        # to False
        portal.REQUEST.RESPONSE.setHeader('Location', 'onlogin_disable')
        registry['collective.onlogin.interfaces.IOnloginSettings.'\
            'login_redirect_enabled'] = False
        userLogin(portal, None)
        self.assertEqual('onlogin_disable',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userLogin_enable_initial_login(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # check when function doesn't doing redirect becouse of providing the
        alsoProvides(portal.REQUEST, IUserInitialLoginInEvent)
        portal.REQUEST.RESPONSE.setHeader('Location', 'affecting_initial_login')
        userLogin(portal, portal.REQUEST)
        self.assertEqual('affecting_initial_login',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userLogin_enable_ignoring_came_from(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # set first onlogin checkbox to disable and no longer provides the
        # initial login
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'first_login_redirect_enabled'] = False

        # checking the ignoring of came_from attribute
        portal.REQUEST['came_from'] = 'some_url'
        portal.REQUEST.RESPONSE.setHeader('Location', 'ignoring_came_from')
        userLogin(portal, portal.REQUEST)
        self.assertEqual('ignoring_came_from',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userLogin_none_expression(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # checking the header when expression of where must be redirecting is
        # None
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'login_redirect_expr'] = u''
        portal.REQUEST.RESPONSE.setHeader('Location', 'without_expression')
        userLogin(portal, None)
        self.assertEqual('without_expression',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userLogin_not_TAL_expression(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # now setting some not suitable expression to check Exception case
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'login_redirect_expr'] = u'not_TAL_expression'

        portal.REQUEST.RESPONSE.setHeader('Location', 'not_correct_expression')
        userLogin(portal, None)
        self.assertEqual('not_correct_expression',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userLogin_with_expression(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # finally setting sutable expression
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'login_redirect_expr'] = u'string:some_url'

        # setting the some header which must be changed on getting expression
        portal.REQUEST.RESPONSE.setHeader('Location', 'not_using')
        userLogin(portal, None)
        self.assertEqual('some_url',
            portal.REQUEST.RESPONSE.getHeader('Location'))

        # and checking case when came_from attribute is not None in the same way
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'login_redirect_expr'] = u'string:some_another_url'
        portal.REQUEST.RESPONSE.setHeader('Location', 'not_using_too')
        portal.REQUEST['came_from'] = 'not_redirect_on_this_page'

        # set the ignoring_came_from becouse of the default value is False
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'login_redirect_ignore_came_from'] = True
        userLogin(portal, portal.REQUEST)
        self.assertEqual('some_another_url',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userInitialLogin_disable_redirect(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # check if our function doesn't doing redirect in our case the header
        # location doesn't changed when the onlogin redirect checkbox is setting
        # to False
        portal.REQUEST.RESPONSE.setHeader('Location', 'onlogin_disable')
        registry['collective.onlogin.interfaces.IOnloginSettings.'\
            'first_login_redirect_enabled'] = False
        userInitialLogin(portal, None)
        self.assertEqual('onlogin_disable',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userInitialLogin_enable_ignoring_came_from(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # checking the ignoring of came_from attribute
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'first_login_redirect_ignore_came_from'] = False
        portal.REQUEST['came_from'] = 'some_url'
        portal.REQUEST.RESPONSE.setHeader('Location', 'ignoring_came_from')
        userInitialLogin(portal, portal.REQUEST)
        self.assertEqual('ignoring_came_from',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userInitialLogin_none_expression(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # checking the header when expression of where must be redirecting is
        # None
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'first_login_redirect_expr'] = u''
        portal.REQUEST.RESPONSE.setHeader('Location', 'without_expression')
        userInitialLogin(portal, None)
        self.assertEqual('without_expression',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userInitialLogin_not_TAL_expression(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)

        # now setting some not sutable expression to check Exception case
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'first_login_redirect_expr'] = u'not_TAL_expression'

        portal.REQUEST.RESPONSE.setHeader('Location', 'not_correct_expression')
        userInitialLogin(portal, None)
        self.assertEqual('not_correct_expression',
            portal.REQUEST.RESPONSE.getHeader('Location'))

    def test_userInitialLogin_with_expression(self):
        portal = self.layer['portal']
        registry = getUtility(IRegistry)
            
        # finally setting sutable expression
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'first_login_redirect_expr'] = u'string:some_url'

        # setting the some header which must be changed on getting expression
        portal.REQUEST.RESPONSE.setHeader('Location', 'not_using')
        userInitialLogin(portal, None)
        self.assertEqual('some_url',
            portal.REQUEST.RESPONSE.getHeader('Location'))

        # and checking case when came_from attribute is not None in the same way
        registry['collective.onlogin.interfaces.IOnloginSettings.' \
            'first_login_redirect_expr'] = u'string:some_another_url'
        portal.REQUEST.RESPONSE.setHeader('Location', 'not_using_too')
        portal.REQUEST['came_from'] = 'not_redirect_on_this_page'
        userInitialLogin(portal, portal.REQUEST)
        self.assertEqual('some_another_url',
            portal.REQUEST.RESPONSE.getHeader('Location'))

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(EventsTests))
    return suite