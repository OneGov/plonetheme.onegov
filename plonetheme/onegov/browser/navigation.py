from ftw.mobilenavigation.browser import navigation
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18n import translate


class SliderNavigation(navigation.SliderNavigation):
    template = ViewPageTemplateFile('slider.pt')


class LoadFlyoutChildren(navigation.UpdateMobileNavigation):
    def __call__(self):
        # Disable theming for ajax requests
        self.request.response.setHeader('X-Theme-Disabled', 'True')

        direct_title = '%s %s' % (
            translate('Direct to', domain="plonetheme.onegov",
                      context=self.request).encode('utf8'),
            self.context.Title())

        subnavi = '<ul class="flyoutChildren">'
        subnavi += '<li class="%s"><a href="%s">%s</a></li>' % (
            'directLink',
            self.context.absolute_url(),
            direct_title
            )
        for obj in self.sub_objects(self.context, level=1):
            subnavi += '<li class="%s"><a href="%s">%s</a></li>' % (
                self.get_css_classes(obj),
                obj.absolute_url(),
                obj.Title())
        subnavi += '</ul>'
        return subnavi
