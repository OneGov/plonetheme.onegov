from ftw.testing import browser
from ftw.testing.pages import Plone


class SearchBox(Plone):

    @property
    def search_field_placeholder(self):
        xpr = '#portal-searchbox input[name=SearchableText]'
        return browser().find_by_css(xpr).first['placeholder']

    @property
    def form_action(self):
        xpr = '#portal-searchbox form'
        return browser().find_by_css(xpr).first['action']

    @property
    def has_solr(self):
        xpr = '#portal-searchbox form.has-solr'
        return len(browser().find_by_css(xpr)) > 0

    @property
    def no_solr(self):
        xpr = '#portal-searchbox form.no-solr'
        return len(browser().find_by_css(xpr)) > 0
