import Missing

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from borg.localrole.interfaces import IFactoryTempFolder
from plone.app.portlets.portlets import base
from plone.app.portlets.portlets.navigation import getRootPath
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('navigation.pt')

    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.parent = aq_parent(aq_inner(context))
        plone = getMultiAdapter((context, request), name="plone")
        self.is_default_page = plone.isDefaultPageInFolder()
        in_factory = IFactoryTempFolder.providedBy(
            self.parent)
        if in_factory:
            self.parent = aq_parent(aq_parent(aq_inner(self.parent)))
        elif self.is_default_page:
            self.parent = aq_parent(aq_inner(self.parent))

    def show_parent(self):
        """ Do not show parent if you are on navigationroot.
        """
        if IPloneSiteRoot.providedBy(self.context):
            return False
        elif self.is_default_page and \
                IPloneSiteRoot.providedBy(aq_parent(aq_inner(self.context))):
            return False
        return True

    def children(self):
        brains = []
        properties = getToolByName(self.context, 'portal_properties')
        hidden_types = properties.navtree_properties.metaTypesNotToList
        for brain in self.context.getFolderContents():
            if brain.portal_type not in hidden_types:
                if getattr(brain, 'exclude_from_nav', False) in \
                        [Missing.Value, False]:
                    brains.append(brain)
        return brains

    @property
    def available(self):
        rootpath = self.getNavRootPath()

        if rootpath is None:
            return False

        return True

    @memoize
    def getNavRootPath(self):
        return getRootPath(self.context, False, 1, None)
