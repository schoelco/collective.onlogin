from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class CollectiveOnlogin(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.onlogin
        xmlconfig.file('configure.zcml',
                       collective.onlogin,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.onlogin:default')

COLLECTIVE_ONLOGIN_FIXTURE = CollectiveOnlogin()
COLLECTIVE_ONLOGIN_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(COLLECTIVE_ONLOGIN_FIXTURE, ),
                       name="CollectiveOnlogin:Integration")