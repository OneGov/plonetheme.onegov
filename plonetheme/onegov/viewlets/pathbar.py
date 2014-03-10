from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PathBarViewlet(common.PathBarViewlet):

    index = ViewPageTemplateFile('pathbar.pt')
