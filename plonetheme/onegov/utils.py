from Products.CMFCore.utils import getToolByName

TIMESTAMP_ANNOTATION_KEY = 'customstyles_url_timestamp'


def replace_custom_keywords(config, context):
    # replace keywords in css output
    portal_url = getToolByName(context, 'portal_url')()
    css_keywords = {
        '%PORTAL_URL%': portal_url,
        '%THEME_URL%': '%s/++theme++plonetheme.onegov' % portal_url
        }

    for search, replace in css_keywords.items():
        config = config.replace(search, replace)
    return config
