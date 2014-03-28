from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import ViewletBase
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.utils import TIMESTAMP_ANNOTATION_KEY


class CustomStyles(ViewletBase):

    index = ViewPageTemplateFile('customstyles.pt')

    def update(self):
        self.css_href = '{}/customstyles_css?ts={}'.format(
            getNavigationRoot(self.context),
            self.timestamp())

    def timestamp(self):
        nav_root = self.context.restrictedTraverse(
            getNavigationRoot(self.context))
        adapter = ICustomStyles(nav_root)
        timestamp = adapter.get(TIMESTAMP_ANNOTATION_KEY)
        if timestamp:
            return timestamp
        return ''
