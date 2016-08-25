from plone import api
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


def is_external_link(brain):
    if brain.portal_type == 'Link':
        url = brain.getRemoteUrl
        if url.startswith('/'):
            # Absolut path - Assume this is a internal link
            return False
        else:
            return not url.startswith(api.portal.get().absolute_url())
    else:
        return False


def get_hostname(request):
    """ Extract hostname from request.
    The scrip is taken from http://docs.plone.org/develop/plone/serving/http_request_and_response.html#hostname
    and includes virtualhost support.
    """

    if "HTTP_X_FORWARDED_HOST" in request.environ:
        host = request.environ["HTTP_X_FORWARDED_HOST"]
    elif "HTTP_HOST" in request.environ:
        host = request.environ["HTTP_HOST"]
    else:
        return ''

    # Remove port
    host = host.split(":")[0].lower()
    return host
