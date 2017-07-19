from ftw.testbrowser import browsing
from plonetheme.onegov.tests import FunctionalTestCase


class TestRendering(FunctionalTestCase):

    @browsing
    def test_theme_is_rendered_anonymous(self, browser):
        browser.login().visit(self.portal)
        self.assertTrue(
            browser.css('#page-wrapper'),
            'Could not find #page-wrapper - was the theme rendered?')

    @browsing
    def test_theme_is_rendered_logged_in(self, browser):
        browser.login().visit(self.portal)
        self.assertTrue(
            browser.css('#page-wrapper'),
            'Could not find #page-wrapper - was the theme rendered?')
