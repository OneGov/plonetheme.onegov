from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import ViewletBase
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.utils import TIMESTAMP_ANNOTATION_KEY


class CustomStyles(ViewletBase):

    index = ViewPageTemplateFile('customstyles.pt')

    def update(self):
        nav_root = self.context.restrictedTraverse(
            getNavigationRoot(self.context))
        self.css_href = '{}/customstyles_css?ts={}'.format(
            nav_root.absolute_url(),
            self.timestamp())

    def timestamp(self):
        nav_root = self.context.restrictedTraverse(
            getNavigationRoot(self.context))
        return ICustomStyles(nav_root).get(TIMESTAMP_ANNOTATION_KEY, '')
