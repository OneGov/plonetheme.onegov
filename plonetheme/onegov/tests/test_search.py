from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plone.browserlayer.layer import mark_layer
from plonetheme.onegov.tests import FunctionalTestCase
from plonetheme.onegov.tests.pages import SearchBox
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.i18n import translate
from zope.interface import alsoProvides
from zope.traversing.interfaces import BeforeTraverseEvent
from zope.viewlet.interfaces import IViewletManager
from ftw.solr.interfaces import IFtwSolrLayer
import transaction


class TestSeachBoxViewlet(FunctionalTestCase):

    def setUp(self):
        super(TestSeachBoxViewlet, self).setUp()
        self.grant('Manager')
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

    @browsing
    def test_default_plone_placeholder_is_used_by_deafult(self, browser):
        browser.visit(self.portal)
        default_placeholder = translate('title_search_site',
                                        default='Search this site',
                                        domain='plone',
                                        context=self.request)
        self.assertEquals(default_placeholder,
                          SearchBox().search_field_placeholder)

    @browsing
    def test_customize_placeholder_by_setting_property(self, browser):
        self.portal._setProperty('search_label', 'Search example.com',
                                 'string')
        transaction.commit()
        browser.visit(self.portal)
        self.assertEquals('Search example.com',
                          SearchBox().search_field_placeholder)

    @browsing
    def test_empty_placeholder_by_setting_property(self, browser):
        self.portal._setProperty('search_label', '', 'string')
        transaction.commit()
        browser.visit(self.portal)
        self.assertEquals('', SearchBox().search_field_placeholder)

    @browsing
    def test_placeholder_property_can_be_overriden_on_any_context(self, browser):
        self.portal._setProperty('search_label', 'search portal', 'string')
        folder = create(Builder('folder'))
        folder._setProperty('search_label', 'search folder', 'string')
        transaction.commit()

        placeholders = {}

        browser.login().visit(self.portal)
        placeholders['portal'] = SearchBox().search_field_placeholder

        browser.visit(folder)
        placeholders['folder'] = SearchBox().search_field_placeholder

        self.assertEquals({'portal': 'search portal',
                           'folder': 'search folder'},
                          placeholders)

    @browsing
    def test_placeholder_property_is_inherited(self, browser):
        self.portal._setProperty('search_label', 'search site', 'string')
        folder = create(Builder('folder'))
        browser.login().visit(folder)
        self.assertEquals('search site', SearchBox().search_field_placeholder)

    @browsing
    def test_form_action_is_page_template_when_solr_disabled(self, browser):
        browser.login().visit(self.portal)
        self.assertEquals('http://nohost/plone/search',
                          SearchBox().form_action)
