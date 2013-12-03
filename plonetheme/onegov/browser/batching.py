from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.batching import browser


class BatchView(browser.PloneBatchView):

    index = template = ViewPageTemplateFile('batchnavigation.pt')
