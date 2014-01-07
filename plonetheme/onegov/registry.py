from collections import defaultdict
from plonetheme.onegov.interfaces import ISCSSRegistry
from zope.interface import Interface
from zope.interface import implements


class SCSSRegistry(object):
    """The registry utility holds the list of .scss files to include.
    The files are ordered.
    """

    implements(ISCSSRegistry)

    def __init__(self):
        self._files = []
        self._removals = defaultdict(list)

    def add_file(self, name, path, for_=Interface, layer=Interface,
                 before=None):
        """Add a new file to the registry.

        The new file may be restricted to certain contexts (with ``for_``)
        or to certain request layers (``layer``).

        The file is appended at the end of the list by default, unless
        ``before`` is set to a name of an already included file, in which case
        the new file is inserted before the existing file. Before should
        contain the ``name`` of the already included file.

        The ``name`` is used for identifying the file and usually consists of
        the package name (where the ZCML is defined) and the relative path
        to the file from the ZCML definition, seperated by a colon.
        Example: ``plonetheme.onegov:components/grid.scss``

        :param name: The name of the file
           (e.g. ``plonetheme.onegov:components/grid.scss``)
        :type name: string
        :param path: The absolute path to the file.
        :type path: string
        :param for_: The context interface required for including this file.
        :type for_: zope.interface.Interface
        :param layer: The request layer interface required for including
           this file.
        :type layer: zope.interface.Interface
        :param before: The name of another file, before the new one
           is inserted.
        :type before: string
        """

        item = {'name': name,
                'path': path,
                'for': for_,
                'layer': layer}

        if self.is_registered(name):
            raise ValueError('The file "%s" is already registered.' % name)

        if before:
            pos = self._position_of(before)
            if pos is None:
                raise ValueError('There is no file "%s" registered.' % before)
            self._files.insert(pos, (name, item))

        else:
            self._files.append((name, item))

    def remove_file(self, name, for_=Interface, layer=Interface):
        """Mark a file to be removed when processing a request.

        A context interface (``for_``) and a request layer interface
        (``layer``) may be defined. Both interface must match the current
        query for the file to be actually removed.

        :param name: The name of the file
          (e.g. ``plonetheme.onegov:components/grid.scss``)
        :type name: string
        :param for_: The context interface required for removing this file.
        :type for_: zope.interface.Interface
        :param layer: The request layer interface required for removing
          this file.
        :type layer: zope.interface.Interface
        """
        if not self.is_registered(name):
            raise ValueError('There is no file "%s" registered.' % name)
        self._removals[name].append((for_, layer))

    def get_files(self, context, request):
        """Get the registered files for the passed ``context`` and ``request``.
        This processes the registry and returns all registered files if their
        context / request conditions match and no removal directive matches.

        The files are returned in the order they are registered.

        :param context: The current context object.
        :param request: The current request object.
        """

        paths = []

        for name, item in self._files:
            if self._is_removed(name, context, request):
                continue
            if not item['for'].providedBy(context):
                continue
            if not item['layer'].providedBy(request):
                continue
            paths.append(item['path'])

        return paths

    def is_registered(self, name):
        """Test if a certain file is registered.

        :param name: The name of the file
          (e.g. ``plonetheme.onegov:components/grid.scss``)
        :type name: string
        :returns: ``True`` when the file is registered.
        :rtype: boolean
        """
        return self._position_of(name) is not None

    def clear(self):
        """Clear the registry.
        """
        self._files = []
        self._removals = defaultdict(list)

    def _position_of(self, name):
        for pos, (item_name, _item) in enumerate(self._files):
            if item_name == name:
                return pos
        return None

    def _is_removed(self, name, context, request):
        if name not in self._removals:
            return False

        for for_, layer in self._removals[name]:
            if not for_.providedBy(context):
                continue
            if not layer.providedBy(request):
                continue
            return True
        return False
