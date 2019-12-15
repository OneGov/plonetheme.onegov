from plone.app.layout.globals.layout import LayoutPolicy


class OnegovLayoutPolicy(LayoutPolicy):
    def bodyClass(self, template, view):
        classes = super(OnegovLayoutPolicy, self).bodyClass(template, view)
        classes = classes.replace('pat-markspeciallinks', '')
        classes += ' pat-markspeciallinks-onegov'
        return classes
