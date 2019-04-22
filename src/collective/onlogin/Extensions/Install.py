# -*- coding: utf-8 -*-

from plone.api.portal import get_tool


PROFILE = 'profile-collective.onlogin:uninstall'


def uninstall(portal):
    setup_tool = get_tool('portal_setup')
    setup_tool.runAllImportStepsFromProfile(PROFILE)
    return 'Ran all uninstall steps.'
