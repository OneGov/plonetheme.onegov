from BTrees.OOBTree import OOBTree
from plone import api
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.layout.viewlets import common
from plonetheme.onegov.utils import replace_custom_keywords
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.interfaces._content import IContentish
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
import pkg_resources


try:
    pkg_resources.get_distribution('ftw.subsite')
except pkg_resources.DistributionNotFound:
    HAS_SUBSITE = False
else:
    from ftw.subsite.interfaces import IFtwSubsiteLayer
    HAS_SUBSITE = True


class LogoViewlet(common.LogoViewlet):

    index = ViewPageTemplateFile('logo.pt')

    def update(self):
        super(LogoViewlet, self).update()
        if HAS_SUBSITE and IFtwSubsiteLayer.providedBy(self.request):
            self.subsite_logo_behaviour()
        else:
            self.onegov_logo_behaviour()

    def onegov_logo_behaviour(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        url = "%s/++theme++plonetheme.onegov/images/logo_onegov.png" % \
            portal.absolute_url()

        annotations = IAnnotations(self.context.restrictedTraverse(
            getNavigationRoot(self.context)))
        customstyles = annotations.get('onegov.customstyles', OOBTree({}))

        if 'img.logo' in customstyles and len(customstyles['img.logo']):
            url = replace_custom_keywords(customstyles['img.logo'],
                                          self.context)

        self.logo_tag = "<img src='%s' alt='%s Logo' />" % (
            url,
            portal.Title())

    def subsite_logo_behaviour(self):
        # Copy of ftw.subsite.viewlets.subsitelogoviewlet
        nav_root = api.portal.get_navigation_root(self.context)
        nav_root_title = nav_root.Title()
        self.navigation_root_url = nav_root.absolute_url()

        if IBaseObject.providedBy(nav_root):
            subsite_logo = nav_root.getLogo()
            subsite_logo_alt_text = nav_root_title

        else:
            subsite_logo = getattr(self.context, 'logo', None)
            subsite_logo_alt_text = getattr(self.context,
                                            'logo_alt_text',
                                            None)

        if subsite_logo and subsite_logo.data:
            # we are in a subsite
            context = self.context
            if not IContentish.providedBy(context):
                context = context.aq_parent
            scale = nav_root.restrictedTraverse('@@images')

            self.logo_tag = scale.scale('logo', scale="logo").tag(
                alt=subsite_logo_alt_text, title=None)
            self.title = nav_root_title
        else:
            # onegov default
            self.onegov_logo_behaviour()
