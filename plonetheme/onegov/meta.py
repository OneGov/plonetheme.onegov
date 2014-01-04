from plonetheme.onegov.interfaces import ISCSSRegistry
from plonetheme.onegov.registry import SCSSRegistry
from zope.component import provideUtility
from zope.component import queryUtility
from zope.configuration.fields import GlobalInterface
from zope.configuration.fields import Path
from zope.interface import Interface
from zope.schema import TextLine
import os.path


class IAddSCSSDirective(Interface):

    path = Path(
        title=u'Path to the .scss file',
        required=True)

    for_ = GlobalInterface(
        title=u'The interface the context should provide.',
        required=False)

    layer = GlobalInterface(
        title=u'The interface the request should provide.',
        required=False)

    before = TextLine(
        title=u'The name of an already added file.',
        description=u'The name usually consists of'
        ' "package:relative file path"',
        required=False)


def add_scss(context, **kwargs):
    """Register an .scss file.
    """

    package_path = os.path.dirname(context.package.__file__)
    relative_path = os.path.relpath(kwargs['path'], package_path)
    name = ':'.join((context.package.__name__, relative_path))

    registry = queryUtility(ISCSSRegistry)
    if registry is None:
        registry = SCSSRegistry()
        provideUtility(registry)

    registry.add_file(name,
                      kwargs['path'],
                      for_=kwargs.get('for_', Interface),
                      layer=kwargs.get('layer', Interface),
                      before=kwargs.get('before', None))


class IRemoveSCSSDirective(Interface):

    name = TextLine(
        title=u'The name of the file to remove.',
        description=u'The name usually consists of'
        ' "package:relative file path"',
        required=True)

    for_ = GlobalInterface(
        title=u'Remove the file only when the context'
        ' provides this interface.',
        required=False)

    layer = GlobalInterface(
        title=u'Remove the file only when the request'
        ' provides this interface.',
        required=False)


def remove_scss(context, **kwargs):
    """Register an .scss file.
    """

    registry = queryUtility(ISCSSRegistry)
    if registry is None:
        registry = SCSSRegistry()
        provideUtility(registry)

    registry.remove_file(kwargs['name'],
                         for_=kwargs.get('for_', Interface),
                         layer=kwargs.get('layer', Interface))
