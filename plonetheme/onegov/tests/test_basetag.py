from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from plonetheme.onegov.tests import FunctionalTestCase


class TestBaseTagViewlet(FunctionalTestCase):

    @browsing
    def test_base_tag_has_trailing_slash(self, browser):
        self.grant('Manager')
        folder = create(Builder('folder').titled(u'The Folder'))
        browser.login().open(folder)
        self.assertEqual({'href': 'http://nohost/plone/the-folder/'},
                         dict(browser.css('base').first.attrib))
