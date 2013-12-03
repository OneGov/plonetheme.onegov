from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.batching import Batch
from plone.browserlayer.layer import mark_layer
from plonetheme.onegov.testing import THEME_FUNCTIONAL_TESTING
from pyquery import PyQuery
from unittest2 import TestCase
from zope.traversing.interfaces import BeforeTraverseEvent


class TestReindering(TestCase):

    layer = THEME_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        mark_layer(self.portal,
                   BeforeTraverseEvent(self.portal, self.request))

    def test_custom_batching_is_available(self):
        batch = Batch.fromPagenumber([item for item in range(1, 100)],
                                    pagesize=10,
                                    pagenumber=1)

        batching = self.portal.restrictedTraverse('@@batchnavigation')

        doc = PyQuery(batching(batch))
        self.assertTrue(doc('.onegovBatching.listingBar'),
                        'Did not found the onegov batching')
