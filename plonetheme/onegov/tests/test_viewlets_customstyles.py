from BTrees.OOBTree import OOBTree
from plone.memoize.interfaces import ICacheChooser
from plonetheme.onegov.interfaces import ISCSSRegistry
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from plonetheme.onegov.viewlets.customstyles import CustomStyles
from unittest2 import TestCase
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility


class TestCustomstylesViewlet(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def test_generates_css_without_error(self):
        viewlet = self.get_viewlet()
        viewlet.update()
        self.assertTrue(viewlet.generate_css())

    def test_result_is_cached(self):
        viewlet = self.get_viewlet()
        viewlet.update()
        self.assertNotIn('purple', viewlet.generate_css(),
                         'Unexpectedly found "purple" in the CSS')

        self.set_style('css.body-background', 'purple')
        self.assertNotIn('purple', viewlet.generate_css(),
                         'The result was not cached.')

        self.invalidate_cache()
        self.assertIn('purple', viewlet.generate_css(),
                      'Expected "purple" in CSS - does the style'
                      ' css.body-background no longer work?')

    def test_css_includes_icon_font(self):
        # REMOVE THIS TEST as soon as it fails!
        viewlet = self.get_viewlet()
        viewlet.update()
        self.assertIn("font-family:'icomoon';", viewlet.generate_css())

    def test_scss_files_registered(self):
        # This is a control sample check that *some* scss files are registered.
        expected = map(lambda name: 'plonetheme.onegov:resources/sass/%s' % name, (
                'mixins.scss',
                'components/base.scss',
                'components/icons.scss',
                'components/menues.scss'))

        registry = getUtility(ISCSSRegistry)
        for name in expected:
            self.assertTrue(registry.is_registered(name),
                            'Expected the scss file "%s" to be registered' % name)

    def set_style(self, name, value):
        # XXX refactor this to use the new customstyles adapter when
        # https://github.com/OneGov/plonetheme.onegov/pull/47 is merged
        context = self.layer['portal']
        annotations = IAnnotations(context)
        key = 'onegov.customstyles'
        if key not in annotations:
            annotations[key] = OOBTree({name: value})
        else:
            annotations[key][name] = value

    def invalidate_cache(self):
        # XXX refactor this to use pt.onegov.viewlets.customstyles.invalidate_cache
        # when https://github.com/OneGov/plonetheme.onegov/pull/47 is merged
        func_name = 'plonetheme.onegov.viewlets.customstyles' + \
            '.CustomStyles.generate_css'
        cache = getUtility(ICacheChooser)(func_name)
        cache.ramcache.invalidateAll()

    def get_viewlet(self):
        context = self.layer['portal']
        request = self.layer['request']
        view = None
        return CustomStyles(context, request, view)
