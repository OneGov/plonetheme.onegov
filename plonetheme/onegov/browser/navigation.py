from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.mobilenavigation.browser import navigation
from zope.i18n import translate


class SliderNavigation(navigation.SliderNavigation):
    template = ViewPageTemplateFile('slider.pt')


class LoadFlyoutChildren(navigation.UpdateMobileNavigation):
    def __call__(self):
        # Disable theming for ajax requests
        self.request.response.setHeader('X-Theme-Disabled', 'True')

        properties = getToolByName(self.context, 'portal_properties')
        self.view_action_types = properties.site_properties.getProperty(
            'typesUseViewActionInListings', ())

        breadcrumbs = self.request.form.get('breadcrumbs', None)
        sub_objects = self.sub_objects(self.context, level=0)
        if breadcrumbs:
            if not sub_objects:
                return ''
            subnavi = '<ul class="children">'
        else:
            direct_title = '%s %s' % (
                translate('Direct to', domain="plonetheme.onegov",
                          context=self.request).encode('utf8'),
                self.context.Title())
            subnavi = '<ul class="flyoutChildren">'
            subnavi += '<li class="%s"><a href="%s">%s</a></li>' % (
                'directLink',
                self.url(self.context),
                direct_title
                )

        for obj in sub_objects:
            subnavi += '<li class="%s"><a href="%s">%s</a></li>' % (
                self.get_css_classes(obj),
                self.url(obj),
                obj.Title())
        subnavi += '</ul>'
        return subnavi

    def url(self, obj):
        if obj.portal_type in self.view_action_types:
            return obj.absolute_url() + '/view'
        return obj.absolute_url()
