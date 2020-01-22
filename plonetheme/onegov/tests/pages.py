from ftw.testbrowser import browser as default_browser
from plone import api


class SearchBox(object):

    def __init__(self, browser=default_browser):
        self.browser = browser
        self.portal = api.portal.get()

    @property
    def search_field_placeholder(self):
        xpr = '#portal-searchbox input[name=SearchableText]'
        return self.browser.css(xpr).first.attrib['placeholder']

    @ property
    def form_action(self):
        xpr = '#portal-searchbox form'
        return self.browser.css(xpr).first.attrib['action']
