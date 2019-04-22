# -*- coding: utf-8 -*-
"""Installer for the collective.onlogin  package."""

from setuptools import find_packages
from setuptools import setup

import os


version = '1.0'

setup(name='collective.onlogin',
      version=version,
      description='This package allows the configuration of HTTP redirects '
                  'after user logs into Plone site.',
      long_description='\n\n'.join([
          open('README.txt').read(),
          open(os.path.join('docs', 'HISTORY.txt')).read(),
      ]),
      # Get more strings from
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: Addon',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
        ],
      keywords='Python Plone redirect login',
      author='Vitaliy Podoba',
      author_email='vitaliy@martinschoel.com',
      url='https://github.com/martinschoel/collective.onlogin',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'test': ['plone.app.testing']},
      install_requires=[
          'setuptools',
          'plone.app.registry',
          # -*- Extra requirements: -*-
          'six',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
