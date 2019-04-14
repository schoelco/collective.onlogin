import unittest

from zope.component import getUtility

from Products.CMFCore.utils import getToolByName

from plone.browserlayer import utils
from plone.registry.interfaces import IRegistry

from collective.onlogin.testing import COLLECTIVE_ONLOGIN_INTEGRATION_TESTING
from collective.onlogin.interfaces import IOnloginLayer


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class InstallTests(unittest.TestCase):

    layer = COLLECTIVE_ONLOGIN_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_browserlayer(self):
        # checking if our IOnloginLayer in the list of installed layers
        self.assertIn(IOnloginLayer, utils.registered_layers())
        
    def test_controlpanel(self):
        cp_tool = getToolByName(self.portal, 'portal_controlpanel')

        # check if our action is added
        self.assertIn('onlogin', [a.id for a in cp_tool.listActions()])

        # get our action out from actions list by id
        for a in cp_tool.listActions():
            if a.id == 'onlogin':
                break

        # test our action settings
        self.assertEqual(a.title, 'Onlogin Settings')
        self.assertEqual(a.appId, 'collective.onlogin')
        self.assertEqual(a.category, 'Products')
        self.assertEqual(a.condition, '')
        self.assertEqual(a.action.text,
            'string:${portal_url}/@@onlogin-settings')
        self.assertEqual(a.visible, True)
        self.assertIn('Manage portal', a.permissions)

    def test_default_registry(self):
        registry = getUtility(IRegistry)

        # checking if the all attributes is enabled
        self.assertEqual(True, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.first_login_redirect_enabled'))
        self.assertEqual(u'string:${portal_url}/@@personal-information',
            registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.first_login_redirect_expr'))
        self.assertEqual(True, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.first_login_redirect_ignore_came_from'))
        self.assertEqual(True, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.login_redirect_enabled'))
        self.assertEqual(u'string:${portal_url}/dashboard',
            registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.login_redirect_expr'))
        self.assertEqual(False, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.login_redirect_ignore_came_from'))

    def test_uninstall_registry(self):
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = self.portal.get_tool('portal_quickinstaller')
        # uninstall collective.onlogin product
        self.installer.uninstall_product('collective.onlogin')

        registry = getUtility(IRegistry)

        # checking if the all attributes is disabled
        self.assertEqual(None, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.first_login_redirect_enabled'))
        self.assertEqual(None, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.first_login_redirect_expr'))
        self.assertEqual(None, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.first_login_redirect_ignore_came_from'))
        self.assertEqual(None, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.login_redirect_enabled'))
        self.assertEqual(None, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.login_redirect_expr'))
        self.assertEqual(None, registry.get('collective.onlogin.interfaces.' \
            'IOnloginSettings.login_redirect_ignore_came_from'))

        # checking if our IOnloginLayer not in the list of installed layers
        self.assertNotIn(IOnloginLayer, utils.registered_layers())

        # checking if our onlogin's skin is disabled
        # check if we got unregistered Directory Views
        skins_tool = getToolByName(self.portal, 'portal_skins')
        self.assertNotIn('collective_onlogin', skins_tool.objectIds())
        self.assertNotIn("collective_onlogin",
            skins_tool._getSelections()['Plone Default'].split(','))
            

        # checking if our onlogin's control_panel disabled
        # check if our onlogin action is disbranched
        self.assertNotIn('onlogin', [a.id for a in getToolByName(self.portal,
            'portal_controlpanel').listActions()])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallTests))
    return suite
