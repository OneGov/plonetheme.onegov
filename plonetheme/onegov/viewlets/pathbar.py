from Acquisition import aq_parent, aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from borg.localrole.interfaces import IFactoryTempFolder
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class PathBarViewlet(common.PathBarViewlet):

    pathbar_flyout = ViewPageTemplateFile('pathbar_flyout.pt')
    pathbar_default = ViewPageTemplateFile('pathbar_default.pt')

    def index(self):
        registry = getUtility(IRegistry)
        if registry.get('plonetheme.onegov.flyout_breadcrumbs', False):
            return self.pathbar_flyout()
        return self.pathbar_default()

    def is_factory(self):
        return IFactoryTempFolder.providedBy(
            aq_parent(aq_inner(self.context)))
