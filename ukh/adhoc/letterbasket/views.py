# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite


from uvc.letterbasket.interfaces import ILetterBasket
from uvc.letterbasket.views import AddThread, AddMessage
from ukhtheme.grok.layout import ILayer

grok.templatedir('templates')


class NachrichtenLP(uvcsite.Page):
    grok.context(ILetterBasket)
    grok.name('index')


#class AddThread(AddThread):
#    grok.require('zope.View')
#    grok.layer(ILayer)


#class AddMessage(AddMessage):
#    grok.name('add')
#    grok.require('zope.View')
#    grok.layer(ILayer)
