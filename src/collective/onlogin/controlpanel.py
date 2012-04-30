from plone.app.registry.browser import controlpanel

from collective.onlogin.interfaces import IOnloginSettings, _


class OnloginSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IOnloginSettings
    label = _(u"Onlogin Settings")
    description = _(u"")

    def updateFields(self):
        super(OnloginSettingsEditForm, self).updateFields()


    def updateWidgets(self):
        super(OnloginSettingsEditForm, self).updateWidgets()

class OnloginSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = OnloginSettingsEditForm
