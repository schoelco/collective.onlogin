from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.onlogin',
      version=version,
      description="This package allows the configuration of HTTP redirects "
          "after user logged in into Plone site.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='redirect login',
      author='Vitaliy Podoba',
      author_email='vitaliy@martinschoel.com',
      url='https://github.com/martinschoel/collective.onlogin',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'test': ['plone.app.testing']},
      install_requires=[
          'setuptools',
          'plone.app.registry',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
