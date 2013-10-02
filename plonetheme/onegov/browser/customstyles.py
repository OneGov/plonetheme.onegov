from BTrees.OOBTree import OOBTree
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from zope.publisher.browser import BrowserView

CUSTOM_STYLE_OPTIONS = [
    "global-navigation-color",
    "global-navigation-color-hover",
    "global-navigation-border-color",
    "global-navigation-border-color-active",
    "highlight-color-light",
    "link-color",
    "link-color-hover",
    ]


class CustomStylesForm(BrowserView):

    template = ViewPageTemplateFile('customstyles_form.pt')

    def __call__(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.fields = CUSTOM_STYLE_OPTIONS
        self.annotations = IAnnotations(portal)

        if self.request.form.get('form.submit', None):
            self.save_values(self.request.form)

        if self.request.form.get('form.reset', None):
            self.save_values({})

        return self.template()

    def save_values(self, items):
        styles = {}
        for key, value in items.items():
            if key.startswith('css.') and value:
                styles[key] = value
        self.annotations['customstyles'] = OOBTree(styles)


    def options(self):
        return self.annotations.get('customstyles', {})
