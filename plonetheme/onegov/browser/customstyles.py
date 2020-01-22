from App.Common import rfc1123_date
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from pathlib import Path
from plone.app.layout.navigation.root import getNavigationRoot
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize import ram
from plone.memoize.interfaces import ICacheChooser
from plone.uuid.interfaces import IUUID
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.interfaces import ISCSSRegistry
from plonetheme.onegov.utils import TIMESTAMP_ANNOTATION_KEY
from plonetheme.onegov.utils import is_debug_mode_enabled
from plonetheme.onegov.utils import replace_custom_keywords
from scss.compiler import Compiler
from scss.source import SourceFile
from zope.component import getUtility
from zope.publisher.browser import BrowserView
import json
import os
import time


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
    "footer-background",
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


def cache_key(method, self):
    cachekey_prefix = '{}.{}'.format(self.__name__, method.__name__)
    # Do not cache if the css debug mode is on
    cssregistry = getToolByName(self.context, 'portal_css')
    if cssregistry.getDebugMode():
        return "{}.{}".format(cachekey_prefix, str(time.time()))
    # Otherwise return the navigation roots uuid
    portal_url = getToolByName(self.context, 'portal_url')()
    nav_root = self.context.restrictedTraverse(getNavigationRoot(self.context))
    uuid = IUUID(nav_root, '/'.join(nav_root.getPhysicalPath()))

    return "{}.{}.{}".format(cachekey_prefix, uuid, portal_url)


def invalidate_cache():
    func_name = 'plonetheme.onegov.viewlets.customstyles' + \
                '.CustomStyles.generate_css'
    cache = getUtility(ICacheChooser)(func_name)
    cache.ramcache.invalidateAll()


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
        adapter = ICustomStyles(self.context)
        styles[TIMESTAMP_ANNOTATION_KEY] = str(time.time()).replace('.','')
        adapter.set_styles(styles)

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

    base_path = os.path.split(__file__)[0]

    def __call__(self):
        response = self.request.response
        response.setHeader("Content-type", "text/css")
        response.setHeader('X-Theme-Disabled', 'True')
        duration = 7.0
        seconds = duration * 24.0 * 3600.0  # 1 day cache duration
        response.setHeader('Expires',
                           rfc1123_date((DateTime() + duration).timeTime()))
        response.setHeader('Cache-Control', 'max-age=%d' % int(seconds))

        return self.generate_css()

    def _get_source_file(self, file):
        path = Path(str(file)).resolve()
        with path.open() as f:
            content = f.read()
        source_file = SourceFile.from_string(content, path)
        source_file.origin = path
        return source_file

    @ram.cache(cache_key)
    def generate_css(self):
        registry = getUtility(ISCSSRegistry)

        # Add default variables
        paths = [Path(self.base_path) / '../resources/sass/variables.scss']
        paths.extend(registry.get_files(self.context, self.request))

        source_files = list(map(self._get_source_file, paths))

        # Add overwritten variables
        options = SourceFile.from_string(self.get_options(),
                                         'plonetheme.onegov/options.scss')
        source_files.insert(1, options)

        compiler = Compiler(
            output_style='expanded' if is_debug_mode_enabled() else 'compressed',
            generate_source_map=True,
        )
        compiled = compiler.compile_sources(*source_files)
        return replace_custom_keywords(compiled, self.context)

    def get_options(self):
        nav_root = self.context.restrictedTraverse(
            getNavigationRoot(self.context))
        options = ICustomStyles(nav_root).get_styles()
        styles = []
        for key, value in options.items():
            if value and key.startswith('css.'):
                styles.append('$%s: %s;' % (key.replace('css.', ''),
                                            value))
            if value and key == 'custom_scss':
                styles.append(value)
        return '\n'.join(styles)
