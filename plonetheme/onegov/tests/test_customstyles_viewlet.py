from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.browser.customstyles import CustomStylesForm
from plonetheme.onegov.testing import THEME_INTEGRATION_TESTING
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from plonetheme.onegov.utils import TIMESTAMP_ANNOTATION_KEY
from plonetheme.onegov.viewlets.customstyles import CustomStyles
from unittest2 import TestCase
from zope.interface import alsoProvides
import transaction


class TestCustomstylesTimestamp(TestCase):
    layer = THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_timestamp_from_annotations(self):
        timestamp = 'a random timestamp'
        ICustomStyles(self.portal).set(TIMESTAMP_ANNOTATION_KEY,
                                       timestamp)
        self.assertEquals(
            timestamp,
            self.get_viewlet(self.portal).timestamp())

    def test_timestamp_not_empty_after_save_styles(self):
        CustomStylesForm(self.portal, self.request).save_values({})
        self.assertNotEquals('', self.get_viewlet(self.portal).timestamp())

    def test_new_timestamp_after_save_styles(self):
        timestamp = 'a random timestamp'
        ICustomStyles(self.portal).set(TIMESTAMP_ANNOTATION_KEY,
                                       timestamp)
        CustomStylesForm(self.portal, self.request).save_values({})
        self.assertNotEquals(
            timestamp,
            self.get_viewlet(self.portal).timestamp())

    def test_timestamp_after_import_styles(self):
        CustomStylesForm(self.portal, self.request).import_styles(
            {TIMESTAMP_ANNOTATION_KEY: 'old timestamp'})
        self.assertNotEquals(
            'old timestamp',
            self.get_viewlet(self.portal).timestamp())

    def get_viewlet(self, context):
        return CustomStyles(context, self.request, None)


class TestCustomstylesViewlet(TestCase):
    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        transaction.commit()

    @browsing
    def test_portal_customcss_path(self, browser):
        browser.login().visit(self.portal)
        self.assertIn(
            '{}/customstyles_css'.format(self.portal.absolute_url()),
            browser.css('head').first.outerHTML)

    @browsing
    def test_subsite_customcss_path(self, browser):
        subsite = self.create_subsite()
        browser.login().visit(subsite)
        self.assertIn(
            '{}/customstyles_css'.format(subsite.absolute_url()),
            browser.css('head').first.outerHTML)

    def create_subsite(self):
        subsite = create(Builder('folder'))
        alsoProvides(subsite, INavigationRoot)
        transaction.commit()
        return subsite
