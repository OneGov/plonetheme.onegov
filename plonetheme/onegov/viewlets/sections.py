from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    index = ViewPageTemplateFile('sections.pt')

    def flyout_enabled(self):
        registry = getUtility(IRegistry)
        return registry.get('plonetheme.onegov.flyout_navigation', False)

    def flyout_grandchildren_enabled(self):
        registry = getUtility(IRegistry)
        return registry.get('plonetheme.onegov.flyout_grandchildren_navigation', False)
