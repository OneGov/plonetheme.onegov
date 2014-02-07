from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets import common
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.utils import replace_custom_keywords


class MetaViewlet(common.LogoViewlet):

    index = ViewPageTemplateFile('meta.pt')

    def update(self):
        super(MetaViewlet, self).update()
        navroot = self.context.restrictedTraverse(
            getNavigationRoot(self.context))
        self.customstyles = ICustomStyles(navroot).get_styles()

        self.favicon = self.customstyle_value('img.favicon') or \
            '/'.join((navroot.absolute_url(), 'favicon.ico'))
        self.startup = self.customstyle_value('img.startup')
        self.touch_iphone = self.customstyle_value('img.touch_iphone')
        self.touch_iphone_76 = self.customstyle_value('img.touch_iphone_76')
        self.touch_iphone_120 = self.customstyle_value('img.touch_iphone_120')
        self.touch_iphone_152 = self.customstyle_value('img.touch_iphone_152')

    def customstyle_value(self, name):
        if name in self.customstyles and len(self.customstyles[name]):
            return replace_custom_keywords(self.customstyles[name],
                                           self.context)
        return None
