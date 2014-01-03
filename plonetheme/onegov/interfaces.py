from zope.interface import Interface


CUSTOMSTYLES_ANNOTATION_KEY = 'onegov.customstyles'


class IPlonethemeOneGovLayer(Interface):
    """Browser layer for plonetheme.onegov
    """


class ICustomStyles(Interface):
    """Adapter for setting and getting custom styles.
    """

    def __init__(context):
        """Adapts a context.
        """

    def get_styles():
        """Returns a dict containing all configured styles.

        :returns: Current custom styles on the context.
        :rtype: dict
        """

    def set_styles(styles):
        """Sets the customstyles.

        :param styles: The new, complete styles to set on the context.
        :type styles: dict
        """

    def set(style, value):
        """Update a single style on the context.

        :param style: Name of the style (e.g. "css.body-background")
        :type style: string
        :param value: The new value of the style.
        :type value: string
        """

    def get(style):
        """Get the current custom style on the context.
        This does NOT get the style from the parent when it is not configured.

        :param style: Name of the style (e.g. "css.body-background")
        :type style: string
        :returns: The value of the style.
        :rtype: string
        """


class ISCSSRegistry(Interface):
    """The registry utility holds the list of .scss files to include.
    The files are ordered.
    """
