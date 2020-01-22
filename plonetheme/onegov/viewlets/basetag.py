from plone.app.layout.viewlets.common import ViewletBase


class BaseTagViewlet(ViewletBase):

    template = '<base href="{}" /><!--[if lt IE 7]></base><![endif]-->'

    def index(self):
        return self.template.format(self.context.absolute_url() + '/')
