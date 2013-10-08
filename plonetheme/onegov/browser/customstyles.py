from AccessControl import getSecurityManager
from BTrees.OOBTree import OOBTree
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.interfaces import ICacheChooser
from zExceptions import Unauthorized
from zope.annotation.interfaces import IAnnotations
from zope.component import queryUtility
from zope.publisher.browser import BrowserView

CUSTOM_STYLE_OPTIONS = [
    "body-background",
    "body-font-family",
    "body-line-height",
    "font-size",
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
    "favicon",
    "startup",
    "touch_iphone",
    "touch_iphone_76",
    "touch_iphone_120",
    "touch_iphone_152",
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
        if not self.can_manage_styles():
            raise Unauthorized
        self.is_subsite = self.context.portal_type == 'Subsite'
        self.css_fields = CUSTOM_STYLE_OPTIONS
        self.img_fields = CUSTOM_IMAGE_PATHS
        self.annotations = IAnnotations(self.context)

        if self.request.form.get('form.submit', None):
            self.save_values(self.request.form)

        if self.request.form.get('form.reset', None):
            self.save_values({})

        return self.template()

    def can_manage_styles(self):
        sm = getSecurityManager()
        return bool(sm.checkPermission('plonetheme.onegov: Manage Styles',
                                       self.context))


    def save_values(self, items):
        styles = {}
        for key, value in items.items():
            if key.startswith('css.') or key.startswith('img.'):
                styles[key] = value
        self.annotations['customstyles'] = OOBTree(styles)
        #invalidate cache
        func_name = 'plonetheme.onegov.viewlets.customstyles.CustomStyles.generate_css'
        cache = queryUtility(ICacheChooser)(func_name)
        cache.ramcache.invalidateAll()



    def options(self):
        return self.annotations.get('customstyles', {})
