from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.mobilenavigation.browser.navigation import escape_html
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

        self.sub_objs = self.sub_objects(self.context, level=0)
        children = []
        for obj in self.sub_objs:
            children.append(u'<li class="%s"><a aria="menuitem" href="%s">%s</a></li>' % (
                self.get_css_classes(obj),
                self.url(obj),
                escape_html(safe_unicode(obj.Title()))))

        return self.children_markup().format(**dict(
            direct_to = self.direct_to_link(),
            children = ''.join(children)))

    def direct_to_link(self):
        direct_title = u'%s %s' % (
            translate('Direct to', domain="plonetheme.onegov",
                      context=self.request).encode('utf8'),
            escape_html(safe_unicode(self.context.Title())))
        return u'<li class="directLink"><a aria="menuitem" href="{}">{}</a></li>'.format(
            self.url(self.context),
            direct_title)

    def children_markup(self):
        breadcrumbs = self.request.form.get('breadcrumbs', None)
        if breadcrumbs:
            if not self.sub_objs:
                return u''
            return u'<ul aria="menu" class="children">{children}</ul>'
        return u'<ul aria="menu" class="flyoutChildren">{direct_to}{children}</ul>'

    def url(self, obj):
        if obj.portal_type in self.view_action_types:
            return obj.absolute_url() + '/view'
        return obj.absolute_url()
