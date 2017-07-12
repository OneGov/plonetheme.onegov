from plone import api
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class OneGovAccessKeysViewlet(ViewletBase):
    index = ViewPageTemplateFile('accesskeys.pt')

    def update(self):
        super(OneGovAccessKeysViewlet, self).update()

        nav_root = api.portal.get_navigation_root(self.context)
        self.nav_root_url = nav_root.absolute_url()
        self.nav_root_title = nav_root.Title()

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self.current_page_url = context_state.current_page_url
