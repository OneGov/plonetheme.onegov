from ftw.testbrowser import browsing
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase


class TestReindering(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    @browsing
    def test_theme_is_rendered_anonymous(self, browser):
        browser.open()
        self.assertTrue(
            browser.css('#page-wrapper'),
            'Could not find #page-wrapper - was the theme rendered?')

    @browsing
    def test_theme_is_rendered_logged_in(self, browser):
        browser.login().open()
        self.assertTrue(
            browser.css('#page-wrapper'),
            'Could not find #page-wrapper - was the theme rendered?')
