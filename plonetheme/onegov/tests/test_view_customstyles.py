from mocker import Mocker
from mocker import expect
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.interfaces import ISCSSRegistry
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from plonetheme.onegov.browser.customstyles import CustomStylesCSS
from plonetheme.onegov.browser.customstyles import invalidate_cache
from unittest2 import TestCase
from zope.component import getUtility


class TestCustomstylesView(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def test_generates_css_without_error(self):
        view = self.get_view()
        self.assertTrue(view.generate_css())

    def test_result_is_cached(self):
        view = self.get_view()
        self.assertNotIn('purple', view.generate_css(),
                         'Unexpectedly found "purple" in the CSS')

        # Setting a custom style automatically invalidates the cache.
        # For testing that things are cached, we stub the cache invalidation,
        # so that the cache persists.
        mocker = Mocker()
        invalidate_cache_mock = mocker.replace(invalidate_cache)
        expect(invalidate_cache_mock()).count(1, None)
        mocker.replay()

        ICustomStyles(self.layer['portal']).set('css.body-background', 'purple')
        self.assertNotIn('purple', view.generate_css(),
                         'The result was not cached.')

        # Removing the stub and invalidating the cache should update the result.
        mocker.restore()
        mocker.verify()
        invalidate_cache()
        self.assertIn('purple', view.generate_css(),
                      'Expected "purple" in CSS - does the style'
                      ' css.body-background no longer work?')

    def test_css_includes_icon_font(self):
        # REMOVE THIS TEST as soon as it fails!
        view = self.get_view()
        self.assertIn("font-family:'icomoon';", view.generate_css())

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

    def get_view(self):
        context = self.layer['portal']
        request = self.layer['request']
        return CustomStylesCSS(context, request)
