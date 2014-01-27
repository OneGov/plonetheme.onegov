from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from plone.memoize.interfaces import ICacheChooser
from plone.uuid.interfaces import IUUID
from plonetheme.onegov.interfaces import ISCSSRegistry
from plonetheme.onegov.utils import replace_custom_keywords
from scss import Scss
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
import os
import time


def cache_key(method, self):
    cachekey_prefix = '{}.{}'.format(self.__name__, method.__name__)
    # Do not cache if the css debug mode is on
    cssregistry = getToolByName(self.context, 'portal_css')
    if cssregistry.getDebugMode():
        return "{}.{}".format(cachekey_prefix, str(time.time()))
    # Otherwise return the navigation roots uuid
    nav_root = self.context.restrictedTraverse(getNavigationRoot(self.context))
    uuid = IUUID(nav_root, '/'.join(nav_root.getPhysicalPath()))
    return "{}.{}".format(cachekey_prefix, uuid)


def invalidate_cache():
    func_name = 'plonetheme.onegov.viewlets.customstyles' + \
        '.CustomStyles.generate_css'
    cache = getUtility(ICacheChooser)(func_name)
    cache.ramcache.invalidateAll()


class CustomStyles(ViewletBase):

    index = ViewPageTemplateFile('customstyles.pt')

    def update(self):
        self.base_path = os.path.split(__file__)[0]
        self.customstyles = self.generate_css()

    @ram.cache(cache_key)
    def generate_css(self):
        css = Scss()
        scss_input = ['@option style:compressed;']
        # add variables
        scss_input.append(self.read_file('variables.scss'))

        # add overwritten variables
        scss_input.append(self.get_options().encode('utf8'))

        # add component files
        registry = getUtility(ISCSSRegistry)
        for path in registry.get_files(self.context, self.request):
            with open(path, 'r') as file_:
                scss_input.append(file_.read())

        # add overwritten component files
        # for now its not possible to add custom styles
        styles = css.compile('\n'.join(scss_input))
        styles = replace_custom_keywords(styles, self.context)
        return styles

    def get_options(self):
        nav_root = self.context.restrictedTraverse(
            getNavigationRoot(self.context))
        options = IAnnotations(nav_root).get('onegov.customstyles', {})
        styles = []
        for key, value in options.items():
            if value and key.startswith('css.'):
                styles.append('$%s: %s;' % (key.replace('css.', ''),
                                            value))
            if value and key == 'custom_scss':
                styles.append(value)
        return '\n'.join(styles)

    def read_file(self, file_path):
        handler = open(os.path.join(
                self.base_path,
                '../resources/sass/%s' % file_path), 'r')
        file_content = handler.read()
        handler.close()
        return file_content
