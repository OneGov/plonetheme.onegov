from setuptools import setup, find_packages
import os

version = '2.0.3'

tests_require = [
    'ftw.builder',
    'ftw.solr',
    'ftw.testbrowser',
    'ftw.subsite',
    'ftw.testing [splinter]',
    'plone.app.testing',
    'plone.resource',
    'pyquery',
    'unittest2',
    ]

setup(name='plonetheme.onegov',
      version=version,
      description="Theme package for OneGov",
      long_description=open("README.rst").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Julian Infanger',
      author_email='julian.infanger@4teamwork.ch',
      url='http://www.4teamwork.ch',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plonetheme'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'plone.app.theming',
        'Products.Archetypes',
        'Products.CMFCore',
        'collective.mtrsetup',
        'ftw.mobilenavigation>=1.2.3',
        'ftw.slider >= 2.1.1',
        'ftw.upgrade',
        'setuptools',
        'plone.batching',
        'PyScss',
        'plone.api',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
