from plonetheme.onegov.interfaces import ICustomStyles
import json

FILENAME = 'customstyles.json'


def importCustomstyles(import_context):
    """Import custom styles defined as a json file named "customstyles.json"
    within any generic setup directory.

    The file contains the exportable JSON and may be extended with a "path" key
    containing the relative path to the target object where the custom styles
    should be set on. When there is no "path", the styles are set on the site
    root.
    """

    filedata = import_context.readDataFile(FILENAME)

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


def exportCustomstyles(export_context):
    """Export custom styles defined on the site root.
    """

    site = export_context.getSite()
    styles = ICustomStyles(site).get_styles()
    data = json.dumps(styles, sort_keys=True, indent=4)
    export_context.writeDataFile(FILENAME, data, 'application/json')
