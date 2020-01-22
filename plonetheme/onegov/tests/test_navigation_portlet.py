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
from plone.registry.interfaces import IRegistry
from plonetheme.onegov.testing import IS_PLONE_5
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase
from unittest2 import skipIf
from zope.component import getUtility
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
        folder = create(Builder('folder').titled(u'The Folder'))
        browser.visit(folder)
        self.assertEquals('The Folder', portlet().css('.current').first.text)

    @browsing
    def test_append_view_to_link_if_type_in_property(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled(u'The Folder'))

        registry = getUtility(IRegistry)
        registry['plone.types_use_view_action_in_listings'] = [u'Image']

        image = create(Builder('image').titled(u'my-image').within(folder))
        # Change the id because DX image get the id from the attached file,
        # not from the title.
        image.aq_parent.manage_renameObject(image.id, 'my-image')
        transaction.commit()

        browser.visit(folder)
        self.assertEqual('http://nohost/plone/the-folder/my-image/view',
                         portlet().css('li.child > a').first.attrib.get('href'))

    @browsing
    def test_dont_append_view_to_link_if_type_in_property(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled(u'The Folder'))

        registry = getUtility(IRegistry)
        registry['plone.types_use_view_action_in_listings'] = []

        image = create(Builder('image').titled(u'my-image').within(folder))
        # Change the id because DX image get the id from the attached file,
        # not from the title.
        image.aq_parent.manage_renameObject(image.id, 'my-image')
        transaction.commit()

        browser.visit(folder)

        self.assertEqual('http://nohost/plone/the-folder/my-image',
                         portlet().css('li.child > a').first.attrib.get('href'))

    @browsing
    def test_lists_children(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled(u'The Folder'))
        create(Builder('page').titled(u'Foo').within(folder))
        create(Builder('page').titled(u'bar').within(folder))
        create(Builder('page').titled(u'Baz').within(folder))

        browser.visit(folder)
        self.assertEquals(['Foo', 'bar', 'Baz'], portlet().css('.child').text)

    @browsing
    def test_does_not_list_content_excluded_from_navigation(self, browser):
        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled(u'The Folder'))
        create(Builder('page').titled(u'Foo').within(folder))
        create(Builder('page').titled(u'Bar').within(folder).having(
                exclude_from_nav=True))

        browser.visit(folder)
        self.assertEquals(['Foo'], portlet().css('.child').text)

    @browsing
    def test_does_not_list_types_excluded_from_navigation(self, browser):
        # Exclude `Document` (AKA `page`) from the navigation:
        registry = getUtility(IRegistry)
        include_types = list(registry['plone.displayed_types'])
        include_types.remove('Document')
        registry['plone.displayed_types'] = tuple(include_types)

        create(Builder('navigation portlet'))
        folder = create(Builder('folder').titled(u'The Folder'))
        create(Builder('page').titled(u'Foo').within(folder))

        browser.visit(folder)
        self.assertEquals([], portlet().css('.child').text)

    @browsing
    def test_lists_siblings_when_configured(self, browser):
        create(Builder('navigation portlet').having(currentFolderOnly=False))
        create(Builder('folder').titled(u'Foo'))
        bar = create(Builder('folder').titled(u'Bar'))
        create(Builder('folder').titled(u'Baz'))

        browser.visit(bar)
        self.assertEquals(['Plone site', 'Foo', 'Bar', 'Baz'],
                          portlet().css('li').text)

    @browsing
    def test_disable_listing_siblings_with_current_folder_only(self, browser):
        create(Builder('navigation portlet').having(currentFolderOnly=True))
        create(Builder('folder').titled(u'Foo'))
        bar = create(Builder('folder').titled(u'Bar'))
        create(Builder('folder').titled(u'Baz'))

        browser.visit(bar)
        self.assertEquals(['Plone site', 'Bar'],
                          portlet().css('li').text)

    @browsing
    def test_siblings_not_shown_when_excluded_from_navigation(self, browser):
        create(Builder('navigation portlet').having(currentFolderOnly=False))
        folder = create(Builder('folder').titled(u'The Folder'))
        create(Builder('folder').titled(u'excluded').having(exclude_from_nav=True))

        browser.visit(folder)
        self.assertEquals(['Plone site', 'The Folder'],
                          portlet().css('li').text)

    @browsing
    def test_siblings_not_shown_when_type_excluded_from_navigation(self, browser):
        # Exclude `Document` (AKA `page`) from the navigation:
        registry = getUtility(IRegistry)
        include_types = list(registry['plone.displayed_types'])
        include_types.remove('Document')
        registry['plone.displayed_types'] = tuple(include_types)

        create(Builder('navigation portlet').having(currentFolderOnly=False))
        folder = create(Builder('folder').titled(u'The Folder'))
        create(Builder('page').titled(u'excluded').having(exclude_from_nav=True))

        browser.visit(folder)
        self.assertEquals(['Plone site', 'The Folder'],
                          portlet().css('li').text)

    @browsing
    def test_workflow_status_class_on_node(self, browser):
        wftool = getToolByName(self.portal, 'portal_workflow')
        wftool.setChainForPortalTypes(['Document', 'Folder'],
                                      'simple_publication_workflow')

        create(Builder('navigation portlet'))
        create(Builder('folder').titled(u'Top Sibling'))
        folder = create(Builder('folder').titled(u'The Folder').in_state('published'))
        create(Builder('page').titled(u'The Page').within(folder))
        create(Builder('folder').titled(u'Bottom Sibling').in_state('pending'))

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
        create(Builder('folder').titled(u'Top Sibling')
               .having(expires=expiration_date))
        folder = create(Builder('folder').titled(u'The Folder')
                        .having(expires=expiration_date))
        create(Builder('page').titled(u'The Page').within(folder)
               .having(expires=expiration_date))
        create(Builder('folder').titled(u'Bottom Sibling')
               .having(expires=expiration_date))

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
        homepage = create(Builder('page').titled(u'Homepage'))
        self.portal._setProperty('default_page', homepage.getId(), 'string')
        homepage.reindexObject()
        other = create(Builder('page').titled(u'Other page'))

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
        parent = create(Builder('folder').titled(u'Parent'))
        create(Builder('folder').titled(u'Top Sibling')
               .within(parent).in_state('published')).reindexObject()
        child = create(Builder('folder').titled(u'Child')
                       .within(parent).in_state('published'))
        sibling = create(Builder('folder').titled(u'Bottom Sibling')
                         .within(parent).in_state('published'))
        sibling.reindexObject()
        create(Builder('folder').titled(u'Child of sibling')
               .within(sibling).in_state('published')).reindexObject()
        transaction.commit()

        browser.open(child)
        self.assertEquals('Parent', portlet().css('.parent').first.text)
        self.assertEquals('Child', portlet().css('.current').first.text)
        self.assertEquals(['Top Sibling', 'Bottom Sibling'],
                          portlet().css('.sibling').text)
