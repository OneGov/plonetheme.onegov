from ftw.builder import Builder
from ftw.builder import create
from ftw.subsite.interfaces import IFtwSubsiteLayer
from plone.app.testing import applyProfile
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2
from plonetheme.onegov.testing import THEME_INTEGRATION_TESTING
from plonetheme.onegov.viewlets.logo import HAS_SUBSITE
from plonetheme.onegov.viewlets.logo import LogoViewlet
from StringIO import StringIO
from unittest2 import TestCase
from zope.interface import alsoProvides
import ftw.subsite.tests.builders


class TestFtwSubsiteLogoBehavior(TestCase):

    layer = THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        z2.installProduct(self.layer['app'], 'ftw.subsite')
        applyProfile(self.portal, 'ftw.subsite:default')

    def _set_logo(self, subsite):
        # 1 x 1 px gif, black
        data = (
            'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00'
            '\x00!\xf9\x04\x04\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00'
            '\x01\x00\x00\x02\x02D\x01\x00;')
        img = StringIO(data)
        img.filename = 'logo.gif'
        subsite.setLogo(img)

    def test_HAS_SUBSITE_is_set(self):
        self.assertTrue(HAS_SUBSITE, 'ftw.subsite is installed.')

    def test_logo_if_subsite_is_available(self):
        request = self.portal.REQUEST
        alsoProvides(request, IFtwSubsiteLayer)

        subsite = create(Builder('subsite').titled('Subsite'))
        self._set_logo(subsite)

        logo_viewlet = LogoViewlet(
            subsite,
            request,
            subsite.restrictedTraverse('@@subsite_view'),
            None)
        logo_viewlet.update()

        # XXX No longer testable, since the subsite has a no longer working 
        # check for the subsite logo

        self.assertIn('width="1"',
                      logo_viewlet.logo_tag,
                      'Expect the width attr in image tag.')

        self.assertIn('height="1"',
                      logo_viewlet.logo_tag,
                      'Expect the height attr in image tag.')

        self.assertIn('alt="{0}"'.format(subsite.Title()),
                      logo_viewlet.logo_tag,
                      'Expect the alt attr in image tag.')

        self.assertIn('src="http://',
                      logo_viewlet.logo_tag,
                      'The src url should start with http (absolute_url not a'
                      ' relative path).')
