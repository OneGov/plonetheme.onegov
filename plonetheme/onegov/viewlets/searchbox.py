from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import pkg_resources


try:
    pkg_resources.get_distribution('ftw.solr')
    from ftw.solr.interfaces import IFtwSolrLayer
except pkg_resources.DistributionNotFound:
    HAS_FTW_SOLR = False
else:
    HAS_FTW_SOLR = True


if HAS_FTW_SOLR:
    from ftw.solr.browser.search import SearchBoxViewlet
else:
    from plone.app.layout.viewlets.common import SearchBoxViewlet


class SearchBoxViewlet(SearchBoxViewlet):
    index = ViewPageTemplateFile('searchbox.pt')

    def has_solr(self):
        return HAS_FTW_SOLR and IFtwSolrLayer.providedBy(self.request)

    def search_action(self):
        if self.has_solr():
            return "%s/@@search" % self.navigation_root_url
        else:
            return "%s/search" % self.navigation_root_url
