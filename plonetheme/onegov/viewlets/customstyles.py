from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets.common import ViewletBase


class CustomStyles(ViewletBase):

    index = ViewPageTemplateFile('customstyles.pt')

    def update(self):
        self.css_href = '{}/customstyles_css'.format(
            getNavigationRoot(self.context))
