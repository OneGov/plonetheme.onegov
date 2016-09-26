import transaction

from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.registry.interfaces import IRegistry
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from zope.component import getUtility


class TestFyloutView(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        transaction.commit()

    @browsing
    def test_view_appended_to_url_if_obj_in_property(self, browser):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings = ('Folder')

        create(Builder('folder'))
        browser.login().visit(view='load_flyout_children')
        self.assertEqual('http://nohost/plone/folder/view',
                         browser.css('.level1 a').first.attrib['href'])

    @browsing
    def test_view_not_appended_to_url_if_obj_not_in_property(self, browser):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings = ('')

        create(Builder('folder'))
        browser.login().visit(view='load_flyout_children')

        self.assertEqual('http://nohost/plone/folder',
                         browser.css('.level1 a').first.attrib['href'])

    @browsing
    def test_direct_link_without_children(self, browser):
        """
        This test makes sure that the direct link is shown even if
        the context has no children.
        """
        create(Builder('folder'))

        browser.login().visit(view='load_flyout_children')

        self.assertTrue(
            browser.css('.directLink'),
            'Direct link is not there but it should.'
        )

    @browsing
    def test_markup_without_direct_link_for_breadcrumbs(self, browser):
        # create a folder, otherwise the breadcrumbs are empty (test below)
        create(Builder('folder'))

        self.request.form.update({'breadcrumbs': '1'})
        browser.login().visit(view='load_flyout_children',
                              data={'breadcrumbs': '1'})

        self.assertFalse(browser.css('.directLink'),
                         'Expect no direct link')

    @browsing
    def test_markup_breadcrumbs_with_no_children(self, browser):
        self.request.form.update({'breadcrumbs': '1'})
        browser.login().visit(view='load_flyout_children',
                              data={'breadcrumbs': '1'})
        self.assertEqual('', browser.contents)

    @browsing
    def test_markup_grandchildren(self, browser):
        folder = create(Builder('folder').titled('My Folder'))
        subfolder = create(Builder('folder').titled(
            u'My Subf\xf6lder').within(folder))
        create(Builder('page').titled(u'My P\xe4ge').within(subfolder))

        registry = getUtility(IRegistry)
        registry['plonetheme.onegov.flyout_grandchildren_navigation'] = True
        transaction.commit()

        browser.open_html(
            subfolder.unrestrictedTraverse('load_flyout_children')())
        self.assertTrue(browser.css('ul.flyoutChildren'))
        self.assertEquals(u'Direct to My Subf\xf6lder',
                          browser.css('.directLink').first.text)
        self.assertEquals(u'My P\xe4ge',
                          browser.css('.level1 a').first.text)
