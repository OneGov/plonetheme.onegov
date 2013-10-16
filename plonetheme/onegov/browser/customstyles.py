import copy
import json

from zope.component import getUtility
from plone.i18n.normalizer.interfaces import IIDNormalizer
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
    "heading-font-family",
    "heading-line-height",
    "heading-font-size",
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

        if self.request.form.get('form.export', None):
            return self.export_styles(download=True)

        if self.request.form.get('form.import', None):
            upload = self.request.form.get('import_styles', None)
            if upload:
                self.import_styles(json.loads(upload.read()))


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
            if key.startswith('css.') or \
                    key.startswith('img.') or \
                    key == 'custom_scss':
                styles[key] = value
        self.annotations['onegov.customstyles'] = OOBTree(styles)
        #invalidate cache
        func_name = 'plonetheme.onegov.viewlets.customstyles.CustomStyles.generate_css'
        cache = queryUtility(ICacheChooser)(func_name)
        cache.ramcache.invalidateAll()

    def export_styles(self, download=False):
        """Returns a json file containing the styles.
        """
        if download:
            normalizer = getUtility(IIDNormalizer)
            normalized_title = normalizer.normalize(self.context.Title())
            self.context.REQUEST.RESPONSE.setHeader(
                'Content-Type',
                'text/json; charset=utf-8')
            self.context.REQUEST.RESPONSE.setHeader(
                'Content-disposition',
                'attachment; filename=customstyles_%s.json' % normalized_title)

        styles = copy.deepcopy(self.annotations['onegov.customstyles'])
        return json.dumps(dict(styles))

    def import_styles(self, styles):
        """Imports styles to annotations.
        """
        self.save_values(items=styles)

    def options(self):
        return self.annotations.get('onegov.customstyles', {})
