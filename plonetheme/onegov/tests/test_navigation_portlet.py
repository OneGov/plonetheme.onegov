from datetime import datetime
from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from ftw.testing import freeze
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
import transaction


def portlet():
    portlets = browser.css('.portletContextNavigation')
    if len(portlets) == 0:
        return None
    else:
        return portlets.first


class TestNavigationPortlet(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    @browsing
    def test_has_parent_link(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder'))
        browser.visit(folder)
        self.assertEquals('Plone site', portlet().css('.parent').first.text)

    @browsing
    def test_shows_current_context_title(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled('The Folder'))
        browser.visit(folder)
        self.assertEquals('The Folder', portlet().css('.current').first.text)

    @browsing
    def test_append_view_to_link_if_type_in_property(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled('The Folder'))

        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=('Image')

        create(Builder('image').titled('my-image').within(folder))
        browser.visit(folder)
        self.assertEqual('http://nohost/plone/the-folder/my-image/view',
                         portlet().css('li.child > a').first.attrib.get('href'))

    @browsing
    def test_dont_append_view_to_link_if_type_in_property(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled('The Folder'))

        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=()

        create(Builder('image').titled('my-image').within(folder))
        browser.visit(folder)

        self.assertEqual('http://nohost/plone/the-folder/my-image',
                         portlet().css('li.child > a').first.attrib.get('href'))

    @browsing
    def test_lists_children(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('page').titled('Foo').within(folder))
        create(Builder('page').titled('bar').within(folder))
        create(Builder('page').titled('Baz').within(folder))

        browser.visit(folder)
        self.assertEquals(['Foo', 'bar', 'Baz'], portlet().css('.child').text)

    @browsing
    def test_does_not_list_content_excluded_from_navigation(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('page').titled('Foo').within(folder))
        create(Builder('page').titled('Bar').within(folder).having(
                excludeFromNav=True))

        browser.visit(folder)
        self.assertEquals(['Foo'], portlet().css('.child').text)

    @browsing
    def test_does_not_list_types_excluded_from_navigation(self, browser):
        properties = getToolByName(self.layer['portal'], 'portal_properties')
        navtree_properties = properties.navtree_properties
        navtree_properties.metaTypesNotToList += ('Document', )

        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('page').titled('Foo').within(folder))

        browser.visit(folder)
        self.assertEquals([], portlet().css('.child').text)

    @browsing
    def test_lists_siblings_when_configured(self, browser):
        create(Builder('navigation portlet').having(currentFolderOnly=False))
        create(Builder('folder').titled('Foo'))
        bar = create(Builder('folder').titled('Bar'))
        create(Builder('folder').titled('Baz'))

        browser.visit(bar)
        self.assertEquals(['Plone site', 'Foo', 'Bar', 'Baz'],
                          portlet().css('li').text)

    @browsing
    def test_disable_listing_siblings_with_current_folder_only(self, browser):
        create(Builder('navigation portlet').having(currentFolderOnly=True))
        create(Builder('folder').titled('Foo'))
        bar = create(Builder('folder').titled('Bar'))
        create(Builder('folder').titled('Baz'))

        browser.visit(bar)
        self.assertEquals(['Plone site', 'Bar'],
                          portlet().css('li').text)

    @browsing
    def test_siblings_not_shown_when_excluded_from_navigation(self, browser):
        create(Builder('navigation portlet').having(currentFolderOnly=False))
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('folder').titled('excluded').having(excludeFromNav=True))

        browser.visit(folder)
        self.assertEquals(['Plone site', 'The Folder'],
                          portlet().css('li').text)

    @browsing
    def test_siblings_not_shown_when_type_excluded_from_navigation(self, browser):
        properties = getToolByName(self.layer['portal'], 'portal_properties')
        navtree_properties = properties.navtree_properties
        navtree_properties.metaTypesNotToList += ('Document', )

        create(Builder('navigation portlet').having(currentFolderOnly=False))
        folder = create(Builder('folder').titled('The Folder'))
        create(Builder('page').titled('excluded').having(excludeFromNav=True))

        browser.visit(folder)
        self.assertEquals(['Plone site', 'The Folder'],
                          portlet().css('li').text)

    @browsing
    def test_workflow_status_class_on_node(self, browser):
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['Document', 'Folder'],
                                      'simple_publication_workflow')

        create(Builder('navigation portlet'))
        create(Builder('folder').titled('Top Sibling'))
        folder = create(Builder('folder').titled('The Folder').in_state('published'))
        create(Builder('page').titled('The Page').within(folder))
        create(Builder('folder').titled('Bottom Sibling').in_state('pending'))

        browser.login().visit(folder)
        self.assertIn('state-private', portlet().css('.sibling')[0].classes)
        self.assertIn('state-published', portlet().css('.current').first.classes)
        self.assertIn('state-private', portlet().css('.child').first.classes)
        self.assertIn('state-pending', portlet().css('.sibling')[1].classes)

    @browsing
    def test_content_expired_class_for_expired_content(self, browser):
        before_expiration = datetime(2010, 1, 1)
        expiration_date = datetime(2010, 2, 2)
        after_expiration = datetime(2010, 3, 3)

        create(Builder('navigation portlet'))
        create(Builder('folder').titled('Top Sibling')
               .having(expirationDate=expiration_date))
        folder = create(Builder('folder').titled('The Folder')
                        .having(expirationDate=expiration_date))
        create(Builder('page').titled('The Page').within(folder)
               .having(expirationDate=expiration_date))
        create(Builder('folder').titled('Bottom Sibling')
               .having(expirationDate=expiration_date))

        with freeze(after_expiration):
            browser.login().visit(folder)
            self.assertIn('content-expired', portlet().css('.sibling')[0].classes)
            self.assertIn('content-expired', portlet().css('.current').first.classes)
            self.assertIn('content-expired', portlet().css('.child').first.classes)
            self.assertIn('content-expired', portlet().css('.sibling')[1].classes)

        with freeze(before_expiration):
            browser.login().visit(folder)
            self.assertNotIn('content-expired', portlet().css('.sibling')[0].classes)
            self.assertNotIn('content-expired',
                             portlet().css('.current').first.classes)
            self.assertNotIn('content-expired', portlet().css('.child').first.classes)
            self.assertNotIn('content-expired', portlet().css('.sibling')[1].classes)

    @browsing
    def test_default_pages_are_not_listed(self, browser):
        create(Builder('navigation portlet'))
        homepage = create(Builder('page').titled('Homepage'))
        self.portal._setProperty('default_page', homepage.getId(), 'string')
        homepage.reindexObject()
        other = create(Builder('page').titled('Other page'))

        browser.open(self.portal)
        self.assertFalse(portlet().css('.parent'))
        self.assertEquals('Homepage', portlet().css('.current').first.text)
        self.assertEquals(['Other page'], portlet().css('.sibling').text)

        browser.open(homepage)
        self.assertFalse(portlet().css('.parent'))
        self.assertEquals('Homepage', portlet().css('.current').first.text)
        self.assertEquals(['Other page'], portlet().css('.sibling').text)

        browser.open(other)
        self.assertEquals('Homepage', portlet().css('.parent').first.text)
        self.assertEquals('Other page', portlet().css('.current').first.text)
        self.assertEquals([], portlet().css('.sibling').text)

    @browsing
    def test_renders_when_parent_not_accessible(self, browser):
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['Folder'], 'simple_publication_workflow')

        create(Builder('navigation portlet').having(currentFolderOnly=False))
        parent = create(Builder('folder').titled('Parent'))
        create(Builder('folder').titled('Top Sibling')
               .within(parent).in_state('published')).reindexObject()
        child = create(Builder('folder').titled('Child')
                       .within(parent).in_state('published'))
        sibling = create(Builder('folder').titled('Bottom Sibling')
                         .within(parent).in_state('published'))
        sibling.reindexObject()
        create(Builder('folder').titled('Child of sibling')
               .within(sibling).in_state('published')).reindexObject()
        transaction.commit()

        browser.open(child)
        self.assertEquals('Parent', portlet().css('.parent').first.text)
        self.assertEquals('Child', portlet().css('.current').first.text)
        self.assertEquals(['Top Sibling', 'Bottom Sibling'],
                          portlet().css('.sibling').text)
