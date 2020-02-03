from Products.CMFPlone.interfaces import ILinkSchema
from Products.CMFPlone.interfaces import IPatternsSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer
import json


@implementer(IPatternsSettings)
class OneGovPatternSettingsAdapter(object):
    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def __call__(self):
        return self.mark_special_links()

    def mark_special_links(self):
        """Settings for plonetheme/onegov/resources/js/pattern.markspeciallinks.js

        Copied from Products.CMFPlone-5.1.6/Products/CMFPlone/patterns/settings.py
        with adjusted pattern name.
        """
        result = {}

        registry = getUtility(IRegistry)
        settings = registry.forInterface(
            ILinkSchema, prefix="plone", check=False)

        msl = settings.mark_special_links
        elonw = settings.external_links_open_new_window
        if msl or elonw:
            result = {
                'data-pat-markspeciallinks-onegov': json.dumps(
                    {
                        'external_links_open_new_window': elonw,
                        'mark_special_links': msl
                    }
                )
            }
        return result
