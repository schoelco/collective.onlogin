import unittest2 as unittest

from zope.component import getUtility

from Products.CMFCore.utils import getToolByName

from plone.browserlayer import utils
from plone.registry.interfaces import IRegistry

from collective.onlogin.testing import COLLECTIVE_ONLOGIN_INTEGRATION_TESTING
from collective.onlogin.interfaces import IOnloginLayer


class InstallTests(unittest.TestCase):

    layer = COLLECTIVE_ONLOGIN_INTEGRATION_TESTING

    def test_browserlayer(self):
        # checking if our IOnloginLayer in the list of installed layers
        self.failUnless(IOnloginLayer in utils.registered_layers())
        
    def test_controlpanel(self):
        cp_tool = getToolByName(self.layer['portal'], 'portal_controlpanel')

        # check if our action is added
        self.failIf('onlogin' not in [a.id for a in cp_tool.listActions()])

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
        self.failIf('Manage portal' not in a.permissions)

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

    def test_skins(self):
        skins_tool = getToolByName(self.layer['portal'], 'portal_skins')

        # check if we got registered Directory Views
        self.failIf('collective_onlogin' not in skins_tool.objectIds())

        # check if layers are added to our skin selection in Plone Default
        layers_default = skins_tool._getSelections()['Plone Default'].split(',')
        self.failIf('collective_onlogin' not in layers_default)

        # check layers order
        idx = lambda name: layers_default.index(name)
        self.assertEqual(idx('collective_onlogin')-1, idx('custom'))

        # check if layers are added to our skin selection in Sunburst Theme
        layers_sunburst = skins_tool._getSelections()['Sunburst Theme']. \
            split(',')
        self.failIf('collective_onlogin' not in layers_sunburst)

        # check layers order
        idx = lambda name: layers_sunburst.index(name)
        self.assertEqual(idx('collective_onlogin')-1, idx('custom'))

    def test_uninstall_registry(self):
        # uninstall collective.onlogin product
        self.layer['portal'].portal_quickinstaller.uninstallProducts(products=
            ['collective.onlogin'])

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
        self.failUnless(IOnloginLayer not in utils.registered_layers())

        # checking if our onlogin's skin is disabled
        # check if we got unregistered Directory Views
        skins_tool = getToolByName(self.layer['portal'], 'portal_skins')
        #import pdb; pdb.set_trace()
        self.failIf('collective_onlogin' in skins_tool.objectIds())
        self.failIf("collective_onlogin" in
            skins_tool._getSelections()['Plone Default'].split(','))
            

        # checking if our onlogin's control_panel disabled
        # check if our onlogin action is disbranched
        self.failIf('onlogin' in [a.id for a in getToolByName(self.layer[
            'portal'], 'portal_controlpanel').listActions()])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallTests))
    return suite