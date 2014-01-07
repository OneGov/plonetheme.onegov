from plonetheme.onegov.interfaces import ISCSSRegistry
from plonetheme.onegov.testing import META_ZCML
from unittest2 import TestCase
from zope.component import getUtility
from zope.configuration.xmlconfig import ZopeXMLConfigurationError
from zope.interface import Interface
from zope.interface import alsoProvides
import os.path


class IFoo(Interface):
    pass


class Context(object):

    def __init__(self, *interfaces):
        for iface in interfaces:
            alsoProvides(self, iface)


class TestRegistryZCML(TestCase):

    layer = META_ZCML

    def test_registering_new_scss_file(self):
        self.load_zcml('<theme:add_scss path="assets/foo.scss" />')

        self.assertEquals([u'assets/foo.scss'], self.get_files())

    def test_error_on_duplicate_registration(self):
        self.load_zcml('<theme:add_scss path="assets/foo.scss" />')
        with self.assertRaises(ZopeXMLConfigurationError) as cm:
            self.load_zcml('<theme:add_scss path="assets/foo.scss" />')

        self.assertIn('The file "plonetheme.onegov.tests:assets/foo.scss"'
                      ' is already registered.',
                      str(cm.exception))

    def test_registering_files_for_specific_context(self):
        self.load_zcml('<theme:add_scss',
                       '    path="assets/foo.scss"',
                       '    for="%s" />' % IFoo.__identifier__)

        self.assertEquals([], self.get_files())
        self.assertEquals([u'assets/foo.scss'], self.get_files(context=Context(IFoo)))

    def test_registering_files_for_request_layer(self):
        self.load_zcml('<theme:add_scss',
                       '    path="assets/foo.scss"',
                       '    layer="%s" />' % IFoo.__identifier__)

        self.assertEquals([], self.get_files())
        self.assertEquals([u'assets/foo.scss'], self.get_files(request=Context(IFoo)))

    def test_register_file_before_another(self):
        self.load_zcml('<theme:add_scss path="assets/foo.scss" />')
        self.load_zcml('<theme:add_scss path="assets/bar.scss" />')
        self.load_zcml('<theme:add_scss path="assets/baz.scss" '
                       '  before="plonetheme.onegov.tests:assets/bar.scss"/>')

        self.assertEquals([u'assets/foo.scss',
                           u'assets/baz.scss',
                           u'assets/bar.scss'],
                          self.get_files())

    def test_register_before_unkown_raises_exception(self):
        with self.assertRaises(ZopeXMLConfigurationError) as cm:
            self.load_zcml('<theme:add_scss path="foo" before="bar" />')

        self.assertIn('There is no file "bar" registered.',
                      str(cm.exception))

    def test_remove_file(self):
        self.load_zcml('<theme:add_scss path="assets/foo.scss" />')
        self.assertEquals([u'assets/foo.scss'], self.get_files())
        self.load_zcml('<theme:remove_scss'
                       ' name="plonetheme.onegov.tests:assets/foo.scss" />')
        self.assertEquals([], self.get_files())

    def test_remove_file_only_on_specific_context(self):
        self.load_zcml('<theme:add_scss path="assets/foo.scss" />')
        self.load_zcml('<theme:remove_scss'
                       ' name="plonetheme.onegov.tests:assets/foo.scss"'
                       ' for="%s" />' % IFoo.__identifier__)

        self.assertEquals([u'assets/foo.scss'], self.get_files())
        self.assertEquals([], self.get_files(context=Context(IFoo)))

    def test_remove_file_only_on_specific_request(self):
        self.load_zcml('<theme:add_scss path="assets/foo.scss" />')
        self.load_zcml('<theme:remove_scss'
                       ' name="plonetheme.onegov.tests:assets/foo.scss"'
                       ' layer="%s" />' % IFoo.__identifier__)

        self.assertEquals([u'assets/foo.scss'], self.get_files())
        self.assertEquals([], self.get_files(request=Context(IFoo)))

    def test_error_when_trying_to_remove_unkown_file(self):
        with self.assertRaises(ZopeXMLConfigurationError) as cm:
            self.load_zcml('<theme:remove_scss name="foo" />')

        self.assertIn('There is no file "foo" registered.',
                      str(cm.exception))

    def load_zcml(self, *lines):
        self.layer.load_zcml_string('\n'.join((
                    '<configure ',
                    '    xmlns:theme="http://namespaces.zope.org/plonetheme.onegov"',
                    '    i18n_domain="my.package"',
                    '    package="plonetheme.onegov.tests"''>',
                    ) + lines +  (
                    '</configure>',
                    )))

    def get_files(self, context=None, request=None):
        registry = getUtility(ISCSSRegistry)
        package_path = os.path.dirname(__file__)
        return map(lambda path: os.path.relpath(path, package_path),
                   registry.get_files(context, request))
