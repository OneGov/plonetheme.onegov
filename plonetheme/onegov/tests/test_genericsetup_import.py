from ftw.builder import Builder
from ftw.builder import create
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase
from zope.interface import alsoProvides
import transaction


def link_color_in(context):
    return ICustomStyles(context).get('css.link-color')


class TestGenericSetupImport(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_portal_customstyles_are_imported(self):
        self.assertEquals(None, link_color_in(self.portal),
                          'No style should be set yet.')
        applyProfile(self.portal, 'plonetheme.onegov.tests:portal-customstyles')
        self.assertEquals('red', link_color_in(self.portal),
                          'Link color style should now be set.')

    def test_foo_customstyles_are_imported(self):
        foo = create(Builder('folder').titled('foo'))
        alsoProvides(foo, INavigationRoot)
        transaction.commit()

        self.assertEquals(None, link_color_in(foo), 'No style should be set yet.')
        applyProfile(self.portal, 'plonetheme.onegov.tests:foo-customstyles')
        self.assertEquals('blue', link_color_in(foo),
                          'Link color style should now be set.')
