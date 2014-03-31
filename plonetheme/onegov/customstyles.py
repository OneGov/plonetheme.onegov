from BTrees.OOBTree import OOBTree
from plone.app.layout.navigation.interfaces import INavigationRoot
from plonetheme.onegov.interfaces import CUSTOMSTYLES_ANNOTATION_KEY
from plonetheme.onegov.interfaces import ICustomStyles
from plonetheme.onegov.browser.customstyles import invalidate_cache
from zope.annotation import IAnnotations
from zope.component import adapts
from zope.interface import implements


class CustomStyles(object):
    implements(ICustomStyles)
    adapts(INavigationRoot)

    def __init__(self, context):
        self.context = context
        self._annotations = None

    def get_styles(self):
        return dict(self.annotations.get(CUSTOMSTYLES_ANNOTATION_KEY, {}))

    def set_styles(self, styles):
        styles = OOBTree(styles)
        self.annotations[CUSTOMSTYLES_ANNOTATION_KEY] = styles
        invalidate_cache()

    def set(self, style, value):
        if not self.annotations.get(CUSTOMSTYLES_ANNOTATION_KEY):
            self.set_styles({style: value})
        else:
            self.annotations[CUSTOMSTYLES_ANNOTATION_KEY][style] = value
            invalidate_cache()

    def get(self, style, fallback=None):
        return self.annotations.get(CUSTOMSTYLES_ANNOTATION_KEY, {}).get(
            style, fallback)

    @property
    def annotations(self):
        if self._annotations is None:
            self._annotations = IAnnotations(self.context)
        return self._annotations
