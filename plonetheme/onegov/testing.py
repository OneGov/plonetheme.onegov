from ftw.builder.content import register_dx_content_builders
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import ComponentRegistryLayer
from pkg_resources import get_distribution
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


IS_PLONE_5 = get_distribution('Plone').version >= '5'


class MetaZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(MetaZCMLLayer, self).setUp()
        import plonetheme.onegov
        self.load_zcml_file('meta.zcml', plonetheme.onegov)


META_ZCML = MetaZCMLLayer()


class ThemeLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        import plonetheme.onegov.tests
        xmlconfig.file('configure.zcml', plonetheme.onegov.tests,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plonetheme.onegov:default')

        applyProfile(portal, 'plone.app.contenttypes:default')
        self.remove_navigation_portlet(portal)

    def remove_navigation_portlet(self, portal):
        """
        Removes the navigation portlet added by "plone.app.contenttypes",
        otherwise we will end up with two portlets in some of our tests
        where the navigation portlet is added manually.
        """
        from plone.portlets.interfaces import IPortletAssignmentMapping
        from plone.portlets.interfaces import IPortletManager
        from zope.component import getMultiAdapter
        from zope.component import getUtility

        manager = getUtility(IPortletManager, name=u'plone.leftcolumn', context=portal)
        assignments = getMultiAdapter((portal, manager), IPortletAssignmentMapping)
        if 'navigation' in assignments:
            del assignments['navigation']


THEME_FIXTURE = ThemeLayer()

THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(THEME_FIXTURE, ),
    name='plonetheme.onegov:integration')

THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(THEME_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="plonetheme.onegov:functional")
