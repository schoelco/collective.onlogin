from zope import schema
from zope.interface import Interface

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.onlogin')


class IOnloginSettings(Interface):

    first_login_redirect_enabled = schema.Bool(
        title=_(u"Enable redirect on first login"),
        description=_(u"First login redirect is of higher priority than "
            "redirect on every login. If disabled, then every login redirect "
            "will be executed even for first time login."),
        required=False,
        default=True)

    first_login_redirect_expr = schema.TextLine(
        title=_(u"First login redirect expression"),
        description=_(u"TAL Expression evaluating to url for first time "
            "redirect."),
        required=False,
        default=u'string:${portal_url}/@@personal-information')

    first_login_redirect_ignore_came_from = schema.Bool(
        title=_(u"Ignore came_from parameter on first login"),
        description=_(u"By default Plone redirects user to last visited page "
            "after login. Here you can disable this behavior and always "
            "redirect to above entered url."),
        required=False,
        default=True)

    login_redirect_enabled = schema.Bool(
        title=_(u"Enable redirect on login"),
        description=_(u"Login redirect is happening on every user login and "
            "does not happen on user first login in case First Login Redirect "
            "is enabled on this form above."),
        required=False,
        default=True)

    login_redirect_expr = schema.TextLine(
        title=_(u"Login redirect expression"),
        description=_(u"TAL Expression evaluating to url for redirect."),
        required=False,
        default=u'string:${portal_url}/dashboard')

    login_redirect_ignore_came_from = schema.Bool(
        title=_(u"Ignore came_from parameter on login"),
        description=_(u"By default Plone redirects user to last visited page "
            "after login. Here you can disable this behavior and always "
            "redirect to above entered url."),
        required=False,
        default=False)


class IOnloginLayer(Interface):
    """Request marker installed via browserlayer.xml"""
