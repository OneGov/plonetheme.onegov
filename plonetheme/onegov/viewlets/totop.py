from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common


class ToTopViewlet(common.ViewletBase):

    index = ViewPageTemplateFile('totop.pt')
