from plonetheme.onegov.registry import SCSSRegistry
from unittest2 import TestCase
from zope.interface import Interface
from zope.interface import alsoProvides


class IFoo(Interface):
    pass


class Context(object):

    def __init__(self, *interfaces):
        for iface in interfaces:
            alsoProvides(self, iface)


class TestSCSSRegistry(TestCase):

    def test_added_files_are_in_ordered_they_are_registered(self):
        registry = SCSSRegistry()
        registry.add_file('bar', 'bar.scss')
        registry.add_file('foo', 'foo.scss')
        registry.add_file('baz', 'baz.scss')

        self.assertEquals(['bar.scss', 'foo.scss', 'baz.scss'],
                          registry.get_files(None, None))

    def test_adding_file_raises_exception_when_file_already_registered(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss')
        with self.assertRaises(ValueError) as cm:
            registry.add_file('foo', 'foo.scss')

        self.assertEquals('The file "foo" is already registered.',
                          str(cm.exception))

    def test_files_are_only_returned_when_context_matches_interface(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss', for_=IFoo)

        self.assertEquals([], registry.get_files(None, None))
        context = Context(IFoo)
        self.assertEquals(['foo.scss'], registry.get_files(context, None))

    def test_files_are_only_returned_when_request_matches_interface(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss', layer=IFoo)

        self.assertEquals([], registry.get_files(None, None))
        request = Context(IFoo)
        self.assertEquals(['foo.scss'], registry.get_files(None, request))

    def test_inserting_file_before_another_file(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss')
        registry.add_file('bar', 'bar.scss')
        registry.add_file('baz', 'baz.scss', before='bar')

        self.assertEquals(['foo.scss', 'baz.scss', 'bar.scss'],
                          registry.get_files(None, None))

    def test_inserting_before_unkown_file_raises_exception(self):
        registry = SCSSRegistry()
        with self.assertRaises(ValueError) as cm:
            registry.add_file('foo', 'foo.scs', before='bar')

        self.assertEquals('There is no file "bar" registered.',
                          str(cm.exception))

    def test_removing_a_file(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss')
        registry.remove_file('foo')

        self.assertEquals([], registry.get_files(None, None))

    def test_removing_a_file_only_when_context_interface_matches(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss')
        registry.remove_file('foo', for_=IFoo)

        self.assertEquals(['foo.scss'], registry.get_files(None, None))
        context = Context(IFoo)
        self.assertEquals([], registry.get_files(context, None))

    def test_removing_a_file_only_when_request_interface_matches(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss')
        registry.remove_file('foo', layer=IFoo)

        self.assertEquals(['foo.scss'], registry.get_files(None, None))
        request = Context(IFoo)
        self.assertEquals([], registry.get_files(None, request))

    def test_removing_unkwown_file_raises_exception(self):
        registry = SCSSRegistry()
        with self.assertRaises(ValueError) as cm:
            registry.remove_file('foo')

        self.assertEquals('There is no file "foo" registered.',
                          str(cm.exception))

    def test_is_registered(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'bar.scss')
        self.assertTrue(registry.is_registered('foo'))
        self.assertFalse(registry.is_registered('bar'))

    def test_clearing_registry(self):
        registry = SCSSRegistry()
        registry.add_file('foo', 'foo.scss')
        self.assertEquals(['foo.scss'], registry.get_files(None, None))

        registry.clear()
        self.assertEquals([], registry.get_files(None, None))
