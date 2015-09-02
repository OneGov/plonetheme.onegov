from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing import ComponentRegistryLayer
from ftw.testing import FunctionalSplinterTesting
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


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


THEME_FIXTURE = ThemeLayer()

THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(THEME_FIXTURE, ),
    name='plonetheme.onegov:integration')

THEME_FUNCTIONAL_TESTING = FunctionalSplinterTesting(
    bases=(THEME_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="plonetheme.onegov:functional")
