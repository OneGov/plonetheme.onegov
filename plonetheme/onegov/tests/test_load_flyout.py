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


class TestFyloutView(TestCase):

    layer = THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        transaction.commit()

        create(Builder('folder'))

    def test_view_appended_to_url_if_obj_in_property(self):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=('Folder')

        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('http://nohost/plone/folder/view',
                         view.url(self.portal.folder))

    def test_view_not_appended_to_url_if_obj_not_in_property(self):
        properties = getToolByName(self.portal, 'portal_properties')
        properties.site_properties.typesUseViewActionInListings=('')

        view = self.portal.unrestrictedTraverse('load_flyout_children')
        view()
        self.assertEqual('http://nohost/plone/folder',
                         view.url(self.portal.folder))
