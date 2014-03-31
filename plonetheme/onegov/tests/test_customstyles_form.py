from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase
from zExceptions import Unauthorized
from zope.interface import alsoProvides
import re
import transaction


class TestCustomstylesForm(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        transaction.commit()

    @browsing
    def test_customstyles_link_works(self, browser):
        browser.login().open()
        browser.find('Manage styles').click()
        self.assertEquals('customstyles_form', plone.view())

    @browsing
    def test_customstyles_link_is_protected_by_permission(self, browser):
        portal = self.layer['portal']
        portal.manage_permission('plonetheme.onegov: Manage Styles',
                                 roles=[], acquire=False)
        transaction.commit()

        browser.login().open()
        self.assertFalse(browser.find('Manage styles'),
                         '"Manage styles" view should not be visible when'
                         ' the user does not have the necessary permission.')

    @browsing
    def test_form_is_available_protected_by_permission(self, browser):
        portal = self.layer['portal']
        portal.manage_permission('plonetheme.onegov: Manage Styles',
                                 roles=[], acquire=False)
        transaction.commit()

        with self.assertRaises(Unauthorized):
            browser.login().visit(view='customstyles_form')

    @browsing
    def test_setting_customstyles_is_persistent(self, browser):
        self.assertEquals(None, self.get_style('css.body-background'),
                          'There should not be a style configured by default.')

        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()

        self.assertEquals('red', self.get_style('css.body-background'))

    @browsing
    def test_resetting_to_defaults(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()
        self.assertEquals('red', self.get_style('css.body-background'))

        browser.find('Reset to OneGov defaults').click()
        self.assertEquals(None, self.get_style('css.body-background'))

    @browsing
    def test_export(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()
        self.assertEquals('red', self.get_style('css.body-background'))

        browser.find('Export styles').click()
        self.assertEquals('red', browser.json['css.body-background'])

    @browsing
    def test_import(self, browser):
        self.assertEquals(None, self.get_style('css.body-background'))
        browser.login().visit(view='customstyles_form')

        styles = '{"css.body-background": "red"}'
        browser.fill({'import_styles': (styles, 'customstyles.json')})
        browser.find('Import styles').click()

        self.assertEquals('red', self.get_style('css.body-background'))

    @browsing
    def test_SUBSITE_set_customstyles_does_not_change_site_root(self, browser):
        subsite = self.create_subsite()
        browser.login().visit(subsite, view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()

        self.assertEquals('red', self.get_style('css.body-background', of=subsite))
        self.assertEquals(None, self.get_style('css.body-background'),
                          'When changing a style on a sub site it should not'
                          ' change it on the site root as well.')

    @browsing
    def test_SUBSITE_resetting_does_not_change_site_root(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()

        subsite = self.create_subsite()
        browser.visit(subsite, view='customstyles_form')
        browser.find('Reset to OneGov defaults').click()

        self.assertEquals('red', self.get_style('css.body-background'),
                          'Resetting styles of a subsite should not change'
                          ' the site root styles.')

    @browsing
    def test_SUBSITE_export_exports_subsite_styles(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()

        subsite = self.create_subsite()
        browser.visit(subsite, view='customstyles_form')
        browser.fill({'Background': 'green'}).submit()

        browser.find('Export styles').click()
        self.assertEquals('green', browser.json['css.body-background'])

    @browsing
    def test_SUBSITE_import_imports_to_subsite(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()

        subsite = self.create_subsite()
        browser.visit(subsite, view='customstyles_form')
        styles = '{"css.body-background": "green"}'
        browser.fill({'import_styles': (styles, 'customstyles.json')})
        browser.find('Import styles').click()

        self.assertEquals('green', self.get_style('css.body-background', of=subsite))
        self.assertEquals('red', self.get_style('css.body-background'))

    @browsing
    def test_copying_styles_between_subsites_with_export_import(self, browser):
        foo = self.create_subsite()
        browser.login().visit(foo, view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()
        browser.find('Export styles').click()
        export = browser.contents

        browser.visit(foo, view='customstyles_form')
        browser.fill({'Background': 'green'}).submit()

        bar = self.create_subsite()
        browser.visit(bar, view='customstyles_form')
        browser.fill({'import_styles': (export, 'customstyles.json')})
        browser.find('Import styles').click()

        self.assertEquals('red', self.get_style('css.body-background', of=bar),
                          'Styles were not imported properly on second subsite')
        self.assertEquals('green', self.get_style('css.body-background', of=foo),
                          'Original subsite was modified on import')

    @browsing
    def test_updating_styles_invalidates_cache(self, browser):
        browser.login().visit(view='customstyles_form')
        browser.fill({'Background': 'red'}).submit()
        self.assertEquals('red', self.get_view_css_body_background())

        browser.fill({'Background': 'green'}).submit()
        self.assertEquals('green', self.get_view_css_body_background())

    def get_view_css_body_background(self):
        css = self.get_view_css()
        xpr = re.compile(r'body\{[^\}]*background:([^;]*);[^\}]*\}')
        matches = xpr.findall(css)
        if len(matches) > 0:
            return matches[0]
        else:
            return None

    def get_view_css(self):
        view = self.layer['portal'].restrictedTraverse('customstyles_css', None)
        if view:
            return view()
        return None

    def get_style(self, style, of=None):
        context = of or self.layer['portal']
        return ICustomStyles(context).get(style)

    def create_subsite(self):
        subsite = create(Builder('folder'))
        alsoProvides(subsite, INavigationRoot)
        transaction.commit()
        return subsite
