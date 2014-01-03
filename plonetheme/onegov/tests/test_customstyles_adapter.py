from BTrees.OOBTree import OOBTree
from plonetheme.onegov.customstyles import CustomStyles
from plonetheme.onegov.interfaces import CUSTOMSTYLES_ANNOTATION_KEY
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.testing import THEME_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.annotation import IAnnotations
from zope.interface.verify import verifyClass


class TestICustomStylesAdapter(TestCase):

    layer = THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_implements_interface(self):
        self.assertTrue(ICustomStyles.implementedBy(CustomStyles))
        verifyClass(ICustomStyles, CustomStyles)

    def test_setting_and_getting_styles(self):
        adapter = ICustomStyles(self.portal)

        styles = {'css.body-background': 'red'}
        adapter.set_styles(styles)
        self.assertEquals(styles, adapter.get_styles())

    def test_mutating_styles_directly_does_not_store_them(self):
        adapter = ICustomStyles(self.portal)

        input = {'css.body-background': 'red'}
        adapter.set_styles(input)

        output = adapter.get_styles()
        self.assertEquals(input, output)

        output['css.body-background'] = 'green'
        self.assertEquals(input, adapter.get_styles(),
                          'The result of get_styles could be modified so that'
                          ' it changed in the storage, which should not happen.')

    def test_setting_and_getting_single_style(self):
        adapter = ICustomStyles(self.portal)

        adapter.set('css.body-background', 'blue')
        self.assertEquals('blue', adapter.get('css.body-background'))

    def test_customstyles_are_stored_in_btree(self):
        adapter = ICustomStyles(self.portal)
        adapter.set('css.body-background', 'blue')

        annotations = IAnnotations(self.portal)
        self.assertEquals(OOBTree, type(annotations.get(CUSTOMSTYLES_ANNOTATION_KEY)))
