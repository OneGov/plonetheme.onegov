from ftw.mobilenavigation.browser import navigation
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SliderNavigation(navigation.SliderNavigation):
    template = ViewPageTemplateFile('slider.pt')
