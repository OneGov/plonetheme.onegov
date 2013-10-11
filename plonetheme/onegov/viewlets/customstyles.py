import os
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import ViewletBase
from plone.memoize import ram
from plone.uuid.interfaces import IUUID
from plonetheme.onegov.browser.customstyles import replace_custom_keywords
from scss import Scss
from zope.annotation.interfaces import IAnnotations


SCSS_FILES = [
    # "components/zug_variables.scss",
    "mixins.scss",
    "components/grid.scss",
    "components/base.scss",
    "components/icons.scss",
    "components/form.scss",
    "components/search.scss",
    "components/tabbedview.scss",
    "components/overlays.scss",
    "components/menues.scss",
    "components/messages.scss",
    "components/tables.scss",
    "components/responsive.scss",
    "components/overrides.scss",
    # "components/overrides_zug.scss",
    ]



def cache_key(method, self):
    uid = IUUID(self.context, str(id(self.context)))
    return 'customstyles-%s' % uid


class CustomStyles(ViewletBase):

    index = ViewPageTemplateFile('customstyles.pt')

    def update(self):
        self.base_path = os.path.split(__file__)[0]
        self.customstyles = self.generate_css()

    @ram.cache(cache_key)
    def generate_css(self):
        css = Scss()
        scss_input = ['@option compress:no;']
        # add variables
        scss_input.append(self.read_file('variables.scss'))

        # add overwritten variables
        scss_input.append(self.get_options().encode('utf8'))

        # add component files
        for scss_file in SCSS_FILES:
            scss_input.append(self.read_file(scss_file))

        # add overwritten component files
        # for now its not possible to add custom styles
        styles = css.compile('\n'.join(scss_input))
        styles = replace_custom_keywords(styles, self.context)
        return styles

    def get_options(self):
        nav_root = self.context.restrictedTraverse(getNavigationRoot(self.context))
        options = IAnnotations(nav_root).get('customstyles', {})
        styles = []
        for key, value in options.items():
            if value:
                styles.append('$%s: %s;' % (key.replace('css.',''),
                                            value))
        if self.request.form.get('print_styles', None):
            print '\n'.join(styles)
        return '\n'.join(styles)

    def read_file(self, file_path):
        handler = open(os.path.join(
                self.base_path,
                '../resources/sass/%s' % file_path), 'r')
        file_content = handler.read()
        handler.close()
        return file_content
