from plonetheme.onegov.interfaces import ICustomStyles
import json


def importCustomstyles(import_context):
    """Import custom styles defined as a json file named "customstyles.json"
    within any generic setup directory.

    The file contains the exportable JSON and may be extended with a "path" key
    containing the relative path to the target object where the custom styles
    should be set on. When there is no "path", the styles are set on the site
    root.
    """

    filedata = import_context.readDataFile('customstyles.json')

    if filedata is None:
        return

    styles = json.loads(filedata)
    site = import_context.getSite()
    if 'path' in styles:
        context = site.restrictedTraverse(styles['path'].encode('utf-8'))
        del styles['path']
    else:
        context = site

    ICustomStyles(context).set_styles(styles)
