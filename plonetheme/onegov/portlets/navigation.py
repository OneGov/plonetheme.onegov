from AccessControl import getSecurityManager
from Acquisition import aq_inner, aq_parent
from borg.localrole.interfaces import IFactoryTempFolder
from plone.app.layout.navigation.defaultpage import getDefaultPage
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.portlets.portlets import base
from plone.app.portlets.portlets.navigation import getRootPath
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import base_hasattr
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
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
        self.view_action_types = properties.site_properties.getProperty(
            'typesUseViewActionInListings', ())

    def show_parent(self):
        """ Do not show parent if you are on navigationroot.
        """
        if IPloneSiteRoot.providedBy(self.context):
            return False
        elif self.is_default_page and \
                IPloneSiteRoot.providedBy(aq_parent(aq_inner(self.context))):
            return False
        return True

    def parent_link(self):
        if getDefaultPage(self.parent):
            page = self.parent.unrestrictedTraverse(
                getDefaultPage(self.parent))
            return {'title': page.Title(),
                    'url': self.parent.absolute_url()}

        else:
            return {'title': self.parent.Title(),
                    'url': self.parent.absolute_url()}

    def siblings(self):
        if self.data.currentFolderOnly:
            return None

        parent = aq_parent(aq_inner(self.context))
        before = []
        after = []
        context_path = '/'.join((self.context.getPhysicalPath()))
        context_reached = False

        catalog = getToolByName(self.context, 'portal_catalog')
        query = {'path': {'query': '/'.join((parent.getPhysicalPath())),
                          'depth': 1},
                 'sort_on': 'getObjPositionInParent'}

        for brain in catalog(query):
            if brain.getPath() == context_path:
                context_reached = True
                continue
            obj = brain.getObject()
            if isDefaultPage(aq_parent(aq_inner(obj)), obj):
                continue
            if not context_reached:
                before.append(brain)
            else:
                after.append(brain)

        return {'before_context': self.filter_brains(before),
                'after_context': self.filter_brains(after)}

    def children(self):
        return self.filter_brains(self.context.getFolderContents())

    def url(self, brain):
        if brain.portal_type in self.view_action_types:
            return brain.getURL() + '/view'
        return brain.getURL()

    def filter_brains(self, brains):
        """Filters brains, removing ignored types and content excluded from
        navigation explictly.
        """
        for brain in brains:
            if brain.portal_type in self.hidden_types:
                continue

            if getattr(brain, 'exclude_from_nav', False):
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

    def cssclasses(self, brain_or_obj):
        classes = []
        if base_hasattr(brain_or_obj, 'getURL'):
            brain = brain_or_obj
            if brain.review_state:
                classes.append('state-%s' % brain.review_state)

            if brain.expires and brain.expires.isPast():
                classes.append('content-expired')

        else:
            obj = brain_or_obj
            context_state = getMultiAdapter((obj, obj.REQUEST),
                                            name='plone_context_state')

            if context_state.workflow_state():
                classes.append('state-%s' % context_state.workflow_state())

            if base_hasattr(obj, 'expires') and obj.expires().isPast():
                classes.append('content-expired')

        return ' '.join(classes)
