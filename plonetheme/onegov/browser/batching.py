from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.batching import browser


class BatchView(browser.PloneBatchView):

    template = ViewPageTemplateFile('batchnavigation.pt')
