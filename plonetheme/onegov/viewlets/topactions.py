from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter


class TopActionsViewlet(ViewletBase):
    index = ViewPageTemplateFile('topactions.pt')

    def update(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        self.top_actions = context_state.actions('top_actions')
