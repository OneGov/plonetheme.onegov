from ftw.testbrowser import browsing
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase
import transaction


class TestMetaViewlet(TestCase):
    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    @browsing
    def test_default_favicon(self, browser):
        browser.open()
        tag = browser.css('link[type="image/x-icon"]').first
        self.assertEquals('http://nohost/plone/favicon.ico',
                          tag.attrib.get('href'))

    @browsing
    def test_favicon_config(self, browser):
        ICustomStyles(self.portal).set('img.favicon', '%PORTAL_URL%/my-fav.ico')
        transaction.commit()
        browser.open()
        tag = browser.css('link[type="image/x-icon"]').first
        self.assertEquals('http://nohost/plone/my-fav.ico',
                          tag.attrib.get('href'))

    @browsing
    def test_startup_image_config(self, browser):
        ICustomStyles(self.portal).set('img.startup', '%PORTAL_URL%/s.png')
        transaction.commit()
        browser.open()
        tag = browser.css('link[rel="apple-touch-startup-image"]').first
        self.assertEquals('http://nohost/plone/s.png',
                          tag.attrib.get('href'))

    @browsing
    def test_touch_iphone_config(self, browser):
        ICustomStyles(self.portal).set('img.touch_iphone', '%PORTAL_URL%/t.png')
        transaction.commit()
        browser.open()
        tag = browser.css('link[rel="apple-touch-icon"]').first
        self.assertEquals('http://nohost/plone/t.png',
                          tag.attrib.get('href'))

    @browsing
    def test_touch_iphone_76_config(self, browser):
        ICustomStyles(self.portal).set('img.touch_iphone_76',
                                       '%PORTAL_URL%/t76.png')
        transaction.commit()
        browser.open()
        tag = browser.css('link[rel="apple-touch-icon"][sizes="76x76"]').first
        self.assertEquals('http://nohost/plone/t76.png',
                          tag.attrib.get('href'))

    @browsing
    def test_touch_iphone_120_config(self, browser):
        ICustomStyles(self.portal).set('img.touch_iphone_120',
                                       '%PORTAL_URL%/t120.png')
        transaction.commit()
        browser.open()
        tag = browser.css('link[rel="apple-touch-icon"][sizes="120x120"]').first
        self.assertEquals('http://nohost/plone/t120.png',
                          tag.attrib.get('href'))

    @browsing
    def test_touch_iphone_152_config(self, browser):
        ICustomStyles(self.portal).set('img.touch_iphone_152',
                                       '%PORTAL_URL%/t152.png')
        transaction.commit()
        browser.open()
        tag = browser.css('link[rel="apple-touch-icon"][sizes="152x152"]').first
        self.assertEquals('http://nohost/plone/t152.png',
                          tag.attrib.get('href'))
