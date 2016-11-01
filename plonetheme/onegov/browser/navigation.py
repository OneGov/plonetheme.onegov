from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from ftw.mobilenavigation.browser import navigation
from plonetheme.onegov.utils import get_hostname
from plonetheme.onegov.utils import is_external_link
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navigation import get_view_url
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.browser.interfaces import IBrowserView
from zope.interface import implements
from zope.publisher.browser import BrowserView
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound
import hashlib
import os


class SliderNavigation(navigation.SliderNavigation):
    template = ViewPageTemplateFile('slider.pt')


class LoadFlyoutChildren(BrowserView):
    """ This view will be called on all breadcrumb-elements
    by the flyoutpathbar.js on pageload.
    For each object a subnavigation will be generated.
    The .js will append the generated html to the path-bar and
    set it visible if you click on the related toplevel-object.
    """

    implements(IPublishTraverse)

    template = ViewPageTemplateFile('flyout.pt')

    def __init__(self, *args, **kwargs):
        super(LoadFlyoutChildren, self).__init__(*args, **kwargs)
        self.cachekey = None

        # When accessing a object of a typesUseViewActionInListings type,
        # self.context may be a view and this view will break.
        # In order to have a proper context we change the context to the
        # parent of the view-context.
        if IBrowserView.providedBy(self.context):
            self.context = aq_parent(aq_inner(self.context))

    def publishTraverse(self, request, name):
        if self.cachekey is not None:
            raise NotFound(self, name, self.request)
        self.cachekey = name
        return self

    def __call__(self):
        self.update()
        self.set_response_headers()

        if len(self.nodes) or not self.is_breadcrumb:
            return self.template()
        else:
            return ""

    def cache_key(self):
        """Returns a cache key (string) which is invalidated as soon
        as objects listed in this flyout are changed.
        The cache key is set to current time when in debug mode.
        """
        portal = getToolByName(self.context, 'portal_url').getPortalObject()

        key = (
            # Including the modified date of the most recent modified
            # item of the base query makes sure that every change of
            # any page changes the cache key.
            # It should only change though when the changed object is
            # actually visible in the flyout navigation.
            str(self.get_last_modified_item_date().millis()),

            # Include hostname. We may connect directly or with differen
            # Domain names (internal / external.
            get_hostname(self.request),

            # Including the template modification timestamp makes sure
            # that when the template changes (e.g. update installed),
            # the cache key is invalidated automatically.
            self.get_template_modified_timestamp(),

            # By including the userid we make sure the cache key is
            # invalidated when another user logs in with the same browser.
            # This is important since the security / visible items may change.
            getSecurityManager().getUser().getId() or '',

            # When the top-level order changes, the site-root's modification
            # date is updated (custom event subscriber).
            # By including the date we make sure that the cache key invalidates
            # when the top-level changes, although this happens rarely.
            str(portal.modified().millis())
        )
        return hashlib.md5('; '.join(key)).hexdigest()

    def get_last_modified_item_date(self):
        """Returns the modified date of the most recent changed item
        included in the query for the flyout.
        Modifed date of the current nav item is returned when there are no
        items.
        """
        catalog = getToolByName(self.context, 'portal_catalog')

        query = self.get_query()
        query['sort_on'] = 'modified'
        query['sort_order'] = 'reverse'
        query['sort_limit'] = 1
        brains = catalog(query)

        last_modified = self.context.modified()

        if brains and brains[0].modified >= last_modified:
            last_modified = brains[0].modified

        return last_modified

    def get_template_modified_timestamp(self):
        page_template = self.template.im_func
        page_template._cook_check()
        if page_template._v_last_read:
            return str(page_template._v_last_read)
        return ''

    def update(self):
        self.is_breadcrumb = self.request.get('breadcrumbs', False)
        self.nodes = self.tree()

    def set_response_headers(self):
        response = self.request.response
        response.setHeader('X-Theme-Disabled', 'True')
        response.enableHTTPCompression(REQUEST=self.request)

        if self.cachekey:
            # Do not set cache headers when no cachekey provided.
            # The cached representation is to be considered fresh for 1 year
            # http://stackoverflow.com/a/3001556/880628
            response.setHeader('Cache-Control', 'private, max-age=31536000')

    def get_brains(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        return [brain for brain in catalog(self.get_query())
                if brain.getPath() != '/'.join(self.context.getPhysicalPath())]

    def get_query(self):
        portal_types = getToolByName(self.context, 'portal_types')
        portal_properties = getToolByName(self.context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')

        exclude_types = getattr(navtree_properties, 'metaTypesNotToList', None)
        include_types = list(set(portal_types.keys()) - set(exclude_types))

        query = {'path': {'query': '/'.join(self.context.getPhysicalPath()),
                          'depth': 2},
                 'portal_type': include_types,
                 'sort_on': 'getObjPositionInParent'}
        return query

    def tree(self):
        return make_tree_by_url(map(self.brain_to_node, self.get_brains()))

    def get_css_class(self, node):
        classes = []
        if len(node.get('nodes', [])) > 0:
            classes.append('noChildren')

        level = int(self.request.form.get('level', '1'))
        classes.append('level{0}'.format(level))
        return ' '.join(classes)

    def brain_to_node(self, brain):
        return {'title': brain.Title,
                'description': brain.Description,
                'url': get_view_url(brain)[1],
                'externallink': is_external_link(brain),
                'exclude_from_nav': brain.exclude_from_nav}


def make_tree_by_url(nodes):
    for node in nodes:
        node['nodes'] = []

    nodes_by_url = dict((node['url'], node) for node in nodes)
    root = []

    for node in nodes:
        parent_url = os.path.dirname(node['url'])
        if parent_url in nodes_by_url:
            nodes_by_url[parent_url]['nodes'].append(node)
        else:
            root.append(node)
    return root
