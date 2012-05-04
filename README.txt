Introduction
============

If you ever wanted to redirect a user right after logging in (e.g. to his/her
personal account dashboard or any other dedicated page) then this package here
is made exactly for this purpose.


Overview
--------

It allows you to configure where to redirect a site user upon logging in.

You also have an option to provide a different redirect for first-time logins.
This feature may be useful in case you want to ask your first time login users
to enter their profile information and/or to set personal preferences.

The ``collective.onlogin`` package provides a Plone control panel where you can
enable redirects as well as set exact URLs where to redirect your users to.


Compatibility
-------------

This add-on was tested for the Plone 4.1 series.


Installation
------------

* to add the package to your Zope instance, please, follow the instructions
  found inside the ``docs/INSTALL.txt`` file
* then restart your Zope instance and install the ``collective.onlogin``
  package from within the ``portal_quickinstaller`` tool


Configuration
-------------

The package provides a configuration panel where you can manage your redirects.
There you have 2 sections:

* for first-time logins,
* and for all next user logins.

First-time login redirects are of higher priority than all the next time
redirects so that the latter will happen only if a user logged in for the second
time or if first-time login redirect is disabled.

Available configuration options:

* ``Enable redirect on first login``. Whether to override default Plone redirect
  on first-time user login. If enabled, it takes precedence over 'next time'
  user login redirects.
* ``First login redirect expression``. TAL Expression for first time login user
  redirect. It should return absolute or relative URL to internal Plone site
  page or absolute URL to any other external web resource. E.g. to redirect to
  external site: ''string:http://google.com''. Default value is to redirect to
  user personal information form within Plone site:
  ''string:${portal_url}/@@personal-information''.
* ``Ignore came_from parameter on first login``. Plone uses came_from query
  parameter in some URLs to be able to redirect back to previously visited page.
  It's usually useful for login procedure. Still you're able to ignore this
  default Plone functionality by ticking this checkbox and ensure user is always
  redirected to a URL you assigned manually in expression mentioned above.
* ``Enable redirect on login``. Override default Plone redirect on user login.
  If user logins for first time then ``First login redirect expression`` will
  take precedence in case first-time redirect is enabled.
* ``Login redirect expression``. TAL Expression for login user redirect. It
  should return absolute or relative URL to internal Plone site page or absolute
  URL to any other external web resource.  Default value is to redirect to
  user personal dashboard: ''string:${portal_url}/@@dashboard''. E.g. to
  redirect user to his/her profile page:
  ''string:${portal_url}/author/${member/getId}''.
* ``Ignore came_from parameter on login``. Ignore default Plone redirect to
  previously visited page before user proceeded to login procedure. Tick this
  checkbox to ensure your manually set redirect is of higher priority over Plone
  'came_from' redirect.


Notes
-----

In order to make the custom redirect event handlers work on user login we had to
disable ajax submits of the default Plone login overlay. Thus we still have a
login overlay but form post is happening as a plain browser request reloading
the whole page.


Live Examples
=============

* http://www.choosehelp.com/


Credits
=======


Companies
---------

|martinschoel|_

* `Martin Schoel Web Productions <http://www.martinschoel.com/>`_
* `Contact us <mailto:python@martinschoel.com>`_


Authors
-------

* Vitaliy Podoba <vitaliy@martinschoel.com>
* Andriy Diedyk <diedyk.andriy@gmail.com>


Contributors
------------


.. |martinschoel| image:: http://cache.martinschoel.com/img/logos/MS-Logo-white-200x100.png
.. _martinschoel: http://www.martinschoel.com/
