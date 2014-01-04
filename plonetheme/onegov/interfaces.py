from zope.interface import Interface


class IPlonethemeOneGovLayer(Interface):
    """Browser layer for plonetheme.onegov
    """


class ISCSSRegistry(Interface):
    """The registry utility holds the list of .scss files to include.
    The files are ordered.
    """
