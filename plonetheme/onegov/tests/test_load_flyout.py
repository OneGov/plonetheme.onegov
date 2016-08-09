import transaction

from Products.CMFCore.utils import getToolByName
from ftw.builder import Builder
from ftw.builder import create
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plonetheme.onegov.testing import THEME_INTEGRATION_TESTING
from unittest2 import TestCase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class TestFyloutView(TestCase):

    layer = THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        transaction.commit()

    def test_view_appended_to_url_if_obj_in_property(self):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=('Folder')

        folder = create(Builder('folder'))
        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('http://nohost/plone/folder/view',
                         view.url(folder))

    def test_view_not_appended_to_url_if_obj_not_in_property(self):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=('')

        folder = create(Builder('folder'))
        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('http://nohost/plone/folder',
                         view.url(folder))

    def test_default_markup_with_direct_link(self):
        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('<ul aria="menu" class="flyoutChildren">{direct_to}{children}</ul>',
                         view.children_markup())

    def test_markup_without_direct_link_for_breadcrumbs(self):
        self.request.form.update({'breadcrumbs': '1'})
        # create a folder, otherwise the breadcrumbs are empty (test below)
        create(Builder('folder'))
        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('<ul aria="menu" class="children">{children}</ul>',
                         view.children_markup())

    def test_markup_breadcrumbs_with_no_children(self):
        self.request.form.update({'breadcrumbs': '1'})
        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('', view.children_markup())

    def test_direct_to_link(self):
        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('<li class="directLink">' \
                         '<a aria="menuitem" href="http://nohost/plone">Direct to Plone site</a>' \
                         '</li>',
                         view.direct_to_link())

    def test_html_chars_are_escaped(self):
        create(Builder('folder').titled(u'<b>SubF\xf6lder</b>'))
        self.request.form.update({'breadcrumbs': '1'})
        self.assertEqual(
            u'<ul aria="menu" class="children"><li class="noChildren level1"><a aria="menuitem" href="http://nohost/plone/b-subfolder-b">&lt;b&gt;SubF\xf6lder&lt;/b&gt;</a></li></ul>',
            self.portal.unrestrictedTraverse('load_flyout_children')())

    def test_html_chars_are_escaped_in_direct_link(self):
        folder = create(Builder('folder').titled(u'<b>SubF\xf6lder</b>'))
        self.assertEqual(
            u'<ul aria="menu" class="flyoutChildren"><li class="directLink"><a aria="menuitem" href="http://nohost/plone/b-subfolder-b">Direct to &lt;b&gt;SubF\xf6lder&lt;/b&gt;</a></li></ul>',
            folder.unrestrictedTraverse('load_flyout_children')())
            
    def test_markup_grandchildren(self):
        folder = create(Builder('folder').titled('My Folder'))
        subfolder = create(Builder('folder').titled(u'My Subf\xf6lder').within(folder))
        create(Builder('page').titled(u'My P\xe4ge').within(subfolder))
        
        registry = getUtility(IRegistry)
        registry['plonetheme.onegov.flyout_grandchildren_navigation'] = True
        transaction.commit()

        self.assertEqual(u'<ul aria="menu" class="flyoutChildren"><li class="directLink"><a aria="menuitem" href="http://nohost/plone/my-folder/my-subfolder">Direct to My Subf\xf6lder</a></li><li class="noChildren level1"><a aria="menuitem" href="http://nohost/plone/my-folder/my-subfolder/my-page">My P\xe4ge</a></li></ul>',
            subfolder.unrestrictedTraverse('load_flyout_children')())
