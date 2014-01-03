from StringIO import StringIO
from ftw.testbrowser import browsing
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase
import json
import tarfile
import transaction


class TestGenericSetupExport(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        transaction.commit()

    @browsing
    def test_generic_setup_exports_customstyles(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()

        browser.visit(view='portal_setup/manage_exportSteps')
        browser.fill({'ids:list': ['plonetheme.onegov.customstyles']})
        browser.find(' Export selected steps ').click()

        self.assertRegexpMatches(browser.headers.get('content-disposition'),
                                 r'attachment; filename=setup_tool-\d*.tar.gz')

        tar = self.read_tarfile(browser)
        self.assertIn('customstyles.json', tar.getnames())
        styles = json.loads(tar.extractfile('customstyles.json').read())
        self.assertEqual('red', styles.get('css.body-background'))

    def read_tarfile(self, browser):
        return tarfile.open(mode='r:gz', fileobj=StringIO(browser.contents))
