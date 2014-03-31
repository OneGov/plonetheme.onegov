from Products.CMFCore.utils import getToolByName

TIMESTAMP_ANNOTATION_KEY = 'customstyles_url_timestamp'


def replace_custom_keywords(config, context):
    # replace keywords in css output
    portal = getToolByName(context, 'portal_url').getPortalObject()
    css_keywords = {
        '%PORTAL_URL%': '/'.join(portal.getPhysicalPath()),
        '%THEME_URL%': '%s/++theme++plonetheme.onegov' % '/'.join(
            portal.getPhysicalPath())}

    for search, replace in css_keywords.items():
        config = config.replace(search, replace)
    return config
