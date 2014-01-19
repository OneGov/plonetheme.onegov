from ftw.builder import builder_registry
from plone.app.portlets.portlets import navigation
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
import transaction


class NavigationPortlet(object):

    def __init__(self, session):
        self.session = session
        self.properties = {}
        self.context = getSite()

    def titled(self, title):
        self.properties['name'] = title
        return self

    def having(self, **kwargs):
        self.properties.update(kwargs)
        return self

    def create(self):
        portlet = self.create_portlet()
        self.after_create(portlet)
        return portlet

    def create_portlet(self):
        portlet = navigation.Assignment(**self.properties)
        manager = getUtility(IPortletManager,
                             name=u'plone.leftcolumn',
                             context=self.context)
        assignments = getMultiAdapter((self.context, manager),
                                      IPortletAssignmentMapping,
                                      context=self.context)
        assignments['navigation'] = portlet

    def after_create(self, portlet):
        if self.session.auto_commit:
            transaction.commit()


builder_registry.register('navigation portlet', NavigationPortlet)
