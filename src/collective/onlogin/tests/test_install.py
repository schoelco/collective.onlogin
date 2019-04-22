# -*- coding: utf-8 -*-


from collective.onlogin import FIRST_ENABLED
from collective.onlogin import FIRST_EXPR
from collective.onlogin import IGNORE_FIRST
from collective.onlogin import IGNORE_REDIRECT
from collective.onlogin import REDIRECT_ENABLED
from collective.onlogin import REDIRECT_EXPR
from collective.onlogin.interfaces import IOnloginLayer
from collective.onlogin.testing import COLLECTIVE_ONLOGIN_INTEGRATION_TESTING
from plone.api.portal import get_tool
from plone.browserlayer import utils
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


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
        cp_tool = get_tool('portal_controlpanel')

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
        self.assertEqual(True, registry.get(FIRST_ENABLED))
        self.assertEqual(u'string:${portal_url}/@@personal-information',
                         registry.get(FIRST_EXPR))
        self.assertEqual(True, registry.get(IGNORE_FIRST))
        self.assertEqual(True, registry.get(REDIRECT_ENABLED))
        self.assertEqual(u'string:${portal_url}/dashboard',
                         registry.get(REDIRECT_EXPR))
        self.assertEqual(False, registry.get(IGNORE_REDIRECT))

    def test_uninstall_registry(self):
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = get_tool('portal_quickinstaller')
        # uninstall collective.onlogin product
        self.installer.uninstall_product('collective.onlogin')

        registry = getUtility(IRegistry)

        # checking if the all attributes is disabled
        self.assertEqual(None, registry.get(FIRST_ENABLED))
        self.assertEqual(None, registry.get(FIRST_EXPR))
        self.assertEqual(None, registry.get(IGNORE_FIRST))
        self.assertEqual(None, registry.get(REDIRECT_ENABLED))
        self.assertEqual(None, registry.get(REDIRECT_EXPR))
        self.assertEqual(None, registry.get(IGNORE_REDIRECT))

        # checking if our IOnloginLayer not in the list of installed layers
        self.assertNotIn(IOnloginLayer, utils.registered_layers())

        # checking if our onlogin's skin is disabled
        # check if we got unregistered Directory Views
        skins_tool = get_tool('portal_skins')
        self.assertNotIn('collective_onlogin', skins_tool.objectIds())
        skinselns = skins_tool._getSelections()['Plone Default'].split(',')
        self.assertNotIn('collective_onlogin', skinselns)

        # checking if our onlogin's control_panel disabled
        # check if our onlogin action is disbranched
        actions = get_tool('portal_controlpanel').listActions()
        self.assertNotIn('onlogin', [a.id for a in actions])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(InstallTests))
    return suite
