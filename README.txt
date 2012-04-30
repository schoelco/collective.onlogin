.. contents::

Introduction
============

This package provides additional functionality of setting the redirecting 
member users when they are login in the portal. In our case we decide to
devide the login user into two parts. The first part is consist of members 
which log in first time and the rest one - the number of users in each time
when they log in the portal.

Installation
============

To install, you must have a enabled package in your buildout.
For example::

    [buildout]
    extends =
        http://pypi.python.org/pypi/collective.onlogin


Usage
=====

Don't forget to activate the package and enter on the following page:
${yourPortalHomePage}/@@onlogin-settings

To enable the redirecting the users on initial login you must set
the following checkbox. "... redirect expression" is the field which has the TAL
condition so you may knew how to write the needed page. In the basic type you
may enter: "string:google.com" to redirect the user to the Google site. If you
need to redirect the user to the specific page of your portal:
"string:${portal_url}/dashboard"
The checkbox of ignoring came_from attribute you may need when you
do not want to redirecting on the page where the user were came from.

In such the same setting is in the second part of settings.
This settings are need in case when you may to redirect the log in member on
every login.

"Enable redirect on first login" checkbox is enabled/disabled the redirecting of
users at the page in "First login redirect expression" when they login in first
time.
By default is True.

"First login redirect expression" is the field with TAL Expression. Here you may
write the page at which you want redirecting users login in first time.
By default is "string:${portal_url}/@@personal-information".

"Ignore came_from parameter on first login" is parameter which may you disable
a Plone default redirecting when the came_from parameter is not None.
By default is True.

"Enable redirect on login" checkbox is enabled/disabled the redirecting of
users at the page in "Login redirect expression" on every login on portal.
By default is True.

"Login redirect expression" is the field with TAL Expression. Here you may
write the page at which you want redirecting users every times when they login
the portal.
By default is "string:${portal_url}/dashboard".

"Ignore came_from parameter on login" is parameter which may you disable
a Plone default redirecting when the came_from parameter is not None.
By default is False.

Compatibility
=============

Plone 4

Authors
=======

