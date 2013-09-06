from ftw.testing import browser
from ftw.testing.pages import Plone
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase


class TestReindering(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def test_theme_is_rendered_anonymous(self):
        Plone().visit_portal()
        self.assertTrue(
            browser().find_by_css('#page-wrapper'),
            'Could not find #page-wrapper - was the theme rendered?')

    def test_theme_is_rendered_logged_in(self):
        Plone().login().visit_portal()
        self.assertTrue(
            browser().find_by_css('#page-wrapper'),
            'Could not find #page-wrapper - was the theme rendered?')
