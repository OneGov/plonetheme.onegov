from simplelayout.base.configlet.interfaces import ISimplelayoutConfiguration
from zope.component import getUtility


def configure_simplelayout(context):
    """Set Simplelayout image sizes.
    """

    SL_CONFIGURATION = {
        'small_size': 204,
        'middle_size': 278,
        'full_size': 648,
        'show_design_tab': False,
        }

    sl_conf = getUtility(ISimplelayoutConfiguration, name='sl-config')
    for key in SL_CONFIGURATION:
        setattr(sl_conf, key, SL_CONFIGURATION[key])


def import_various(context):
    """Miscellanous steps import handle
    """

    if context.readDataFile('plonetheme.onegov_various.txt') is None:
        return

    portal = context.getSite()

    configure_simplelayout(portal)
