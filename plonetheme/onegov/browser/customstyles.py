from BTrees.OOBTree import OOBTree
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from zope.publisher.browser import BrowserView

CUSTOM_STYLE_OPTIONS = [
    "body-background",
    "global-navigation-color",
    "global-navigation-color-hover",
    "global-navigation-border-color",
    "global-navigation-border-color-active",
    "highlight-color-light",
    "link-color",
    "link-color-hover",
    ]

CUSTOM_IMAGE_PATHS = [
    "logo",
    "favico",
    ]


def replace_custom_keywords(config, context):
    #replace keywords in css output
    portal = getToolByName(context, 'portal_url').getPortalObject()
    css_keywords = {
        '%PORTAL_URL%': '/'.join(portal.getPhysicalPath()),
        '%THEME_URL%': '%s/++theme++plonetheme.onegov' % '/'.join(portal.getPhysicalPath())}

    for search, replace in css_keywords.items():
        config = config.replace(search, replace)
    return config


class CustomStylesForm(BrowserView):

    template = ViewPageTemplateFile('customstyles_form.pt')

    def __call__(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        self.css_fields = CUSTOM_STYLE_OPTIONS
        self.img_fields = CUSTOM_IMAGE_PATHS
        self.annotations = IAnnotations(portal)

        if self.request.form.get('form.submit', None):
            self.save_values(self.request.form)

        if self.request.form.get('form.reset', None):
            self.save_values({})

        return self.template()

    def save_values(self, items):
        styles = {}
        for key, value in items.items():
            if key.startswith('css.') or key.startswith('img.'):
                styles[key] = value
        self.annotations['customstyles'] = OOBTree(styles)


    def options(self):
        return self.annotations.get('customstyles', {})
