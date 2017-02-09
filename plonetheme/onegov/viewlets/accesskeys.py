from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OneGovSkipLinksViewlet(common.SkipLinksViewlet):
    index = ViewPageTemplateFile('accesskeys.pt')

    def update(self):
        super(OneGovSkipLinksViewlet, self).update()
        nav_root = api.portal.get_navigation_root(self.context)
        self.nav_root_url = nav_root.absolute_url()
        self.nav_root_title = nav_root.Title()
