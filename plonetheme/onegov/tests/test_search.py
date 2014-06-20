from Products.Five.browser import BrowserView
from ftw.builder import Builder
from ftw.builder import create
from ftw.solr.interfaces import IFtwSolrLayer
from ftw.testing.pages import Plone
from plone.app.testing import TEST_USER_ID
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.browserlayer.layer import mark_layer
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from plonetheme.onegov.tests.pages import SearchBox
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.traversing.interfaces import BeforeTraverseEvent
from zope.viewlet.interfaces import IViewletManager
import transaction


class TestSeachBoxViewlet(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        mark_layer(self.portal,
                   BeforeTraverseEvent(self.portal, self.request))

    def get_viewlet(self, context):
        view = BrowserView(context, context.REQUEST)
        manager_name = 'plone.portalheader'
        manager = queryMultiAdapter(
            (context, context.REQUEST, view),
            IViewletManager,
            manager_name)
        self.assertTrue(manager, 'Could not find %s viewlet manager' % (
                manager_name))

        # Set up viewlets
        manager.update()
        name = 'plone.searchbox'
        return [v for v in manager.viewlets if v.__name__ == name][0]

    def test_has_solr_is_false_by_default(self):
        viewlet = self.get_viewlet(self.portal)
        self.assertFalse(viewlet.has_solr())

    def test_when_request_is_marked_with_requestlayer_has_solr_is_true(self):
        viewlet = self.get_viewlet(self.portal)
        alsoProvides(self.portal.REQUEST, IFtwSolrLayer)

        self.assertTrue(viewlet.has_solr())

    def test_default_plone_placeholder_is_used_by_deafult(self):
        Plone().visit_portal()
        default_placeholder = translate('title_search_site',
                                        default='Search this site',
                                        domain='plone',
                                        context=self.request)
        self.assertEquals(default_placeholder,
                          SearchBox().search_field_placeholder)

    def test_customize_placeholder_by_setting_property(self):
        self.portal._setProperty('search_label', 'Search example.com',
                                 'string')
        transaction.commit()
        Plone().visit_portal()
        self.assertEquals('Search example.com',
                          SearchBox().search_field_placeholder)

    def test_empty_placeholder_by_setting_property(self):
        self.portal._setProperty('search_label', '', 'string')
        transaction.commit()
        Plone().visit_portal()
        self.assertEquals('', SearchBox().search_field_placeholder)

    def test_placeholder_property_can_be_overriden_on_any_context(self):
        self.portal._setProperty('search_label', 'search portal', 'string')
        folder = create(Builder('folder'))
        folder._setProperty('search_label', 'search folder', 'string')
        transaction.commit()

        placeholders = {}

        Plone().login().visit_portal()
        placeholders['portal'] = SearchBox().search_field_placeholder
        Plone().visit(folder)
        placeholders['folder'] = SearchBox().search_field_placeholder

        self.assertEquals({'portal': 'search portal',
                           'folder': 'search folder'},
                          placeholders)

    def test_placeholder_property_is_inherited(self):
        self.portal._setProperty('search_label', 'search site', 'string')
        folder = create(Builder('folder'))
        Plone().login().visit(folder)
        self.assertEquals('search site', SearchBox().search_field_placeholder)

    def test_form_action_is_page_template_when_solr_disabled(self):
        Plone().login().visit_portal()
        self.assertEquals('http://nohost/plone/search',
                          SearchBox().form_action)

    def test_no_solr_cssclass_present_when_solr_disabled(self):
        Plone().login().visit_portal()
        self.assertTrue(SearchBox().no_solr,
                        'The no-solr class is missing on the search <form>')
        self.assertFalse(SearchBox().has_solr,
                         'There is a has-solr AND a no-solr class!?')


class TestSeachBoxViewletWithSolr(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        request = self.layer['request']
        applyProfile(portal, 'ftw.solr:default')
        mark_layer(portal, BeforeTraverseEvent(portal, request))
        transaction.commit()

    def test_form_action_is_view_when_solr_enabled(self):
        Plone().login().visit_portal()
        self.assertEquals('http://nohost/plone/@@search',
                          SearchBox().form_action)

    def test_has_solr_cssclass_present_when_solr_enabled(self):
        Plone().login().visit_portal()
        self.assertTrue(SearchBox().has_solr,
                        'The has-solr class is missing on the search <form>')
        self.assertFalse(SearchBox().no_solr,
                         'There is a has-solr AND a no-solr class!?')
