from ftw.testbrowser import browsing
from plone.app.testing import login
from plone.app.testing import setRoles
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import transaction


class TestFlyoutNavigationViewlet(TestCase):
    layer = THEME_FUNCTIONAL_TESTING

    @browsing
    def test_flyout_navigation_is_enabled(self, browser):
        browser.open()
        self.assertIn(
            'flyoutEnabled',
            browser.css('#portal-globalnav').first.classes)

    @browsing
    def test_flyout_navigation_is_disabled(self, browser):
        registry = getUtility(IRegistry)
        registry['plonetheme.onegov.flyout_navigation'] = False
        transaction.commit()

        browser.open()
        self.assertNotIn(
            'flyoutEnabled',
            browser.css('#portal-globalnav').first.classes)

    @browsing
    def test_flyout_navigation_is_enabled(self, browser):
        browser.open()
        self.assertNotIn(
            'flyoutGrandchildrenEnabled',
            browser.css('#portal-globalnav').first.classes)

    @browsing
    def test_flyout_navigation_is_disabled(self, browser):
        registry = getUtility(IRegistry)
        registry['plonetheme.onegov.flyout_grandchildren_navigation'] = True
        transaction.commit()

        browser.open()
        self.assertIn(
            'flyoutGrandchildrenEnabled',
            browser.css('#portal-globalnav').first.classes)
