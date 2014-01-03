from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.viewlets.customstyles import CustomStyles
from zope.component import getUtility
from zope.publisher.browser import BrowserView
import json


CUSTOM_STYLE_OPTIONS = [
    "body-background",
    "heading-font-family",
    "heading-line-height",
    "heading-font-size",
    "global-navigation-color",
    "global-navigation-color-hover",
    "global-navigation-color-selected",
    "global-navigation-border-color",
#    "global-navigation-border-color-active",
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


class CustomStylesForm(BrowserView):

    template = ViewPageTemplateFile('customstyles_form.pt')

    def __call__(self):
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

        return self.render()

    def render(self):
        self.is_subsite = self.context.portal_type == 'Subsite'
        self.css_fields = CUSTOM_STYLE_OPTIONS
        self.img_fields = CUSTOM_IMAGE_PATHS
        return self.template()

    def save_values(self, items):
        def include(item):
            name, _value = item
            if name.startswith('css.'):
                return True
            if name.startswith('img.'):
                return True
            if name == 'custom_scss':
                return True
            return False

        styles = dict(filter(include, items.items()))
        ICustomStyles(self.context).set_styles(styles)

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

        return json.dumps(ICustomStyles(self.context).get_styles())

    def import_styles(self, styles):
        """Imports styles to annotations.
        """
        self.save_values(items=styles)

    def options(self):
        return ICustomStyles(self.context).get_styles()


class CustomStylesCSS(BrowserView):

    def __call__(self):
        css_viewlet = CustomStyles(self.context, self.request, self)
        css_viewlet.update()
        return css_viewlet.customstyles
