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
        self.data = data
        plone = getMultiAdapter((context, request), name="plone")
        self.is_default_page = plone.isDefaultPageInFolder()
        in_factory = IFactoryTempFolder.providedBy(
            self.parent)
        if in_factory:
            self.parent = aq_parent(aq_parent(aq_inner(self.parent)))
        elif self.is_default_page:
            self.parent = aq_parent(aq_inner(self.parent))

        properties = getToolByName(self.context, 'portal_properties')
        self.hidden_types = properties.navtree_properties.metaTypesNotToList

    def show_parent(self):
        """ Do not show parent if you are on navigationroot.
        """
        if IPloneSiteRoot.providedBy(self.context):
            return False
        elif self.is_default_page and \
                IPloneSiteRoot.providedBy(aq_parent(aq_inner(self.context))):
            return False
        return True

    def siblings(self):
        if self.data.currentFolderOnly:
            return None

        parent = aq_parent(aq_inner(self.context))
        before = []
        after = []
        context_path = '/'.join((self.context.getPhysicalPath()))
        context_reached = False

        for brain in parent.getFolderContents():
            if brain.getPath() == context_path:
                context_reached = True
                continue
            if not context_reached:
                before.append(brain)
            else:
                after.append(brain)

        return {'before_context': self.filter_brains(before),
                'after_context': self.filter_brains(after)}

    def children(self):
        return self.filter_brains(self.context.getFolderContents())

    def filter_brains(self, brains):
        """Filters brains, removing ignored types and content excluded from
        navigation explictly.
        """
        for brain in brains:
            if brain.portal_type in self.hidden_types:
                continue

            if getattr(brain, 'exclude_from_nav', False) == True:
                continue

            yield brain

    @property
    def available(self):
        rootpath = self.getNavRootPath()

        if rootpath is None:
            return False

        return True

    @memoize
    def getNavRootPath(self):
        return getRootPath(self.context, False, 1, None)
