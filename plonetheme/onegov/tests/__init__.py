from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from unittest2 import TestCase
import transaction


class FunctionalTestCase(TestCase):
    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()
