# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite


from ukh.adhoc.interfaces import IUKHAdHocApp


class Index(uvcsite.Page):
    grok.context(IUKHAdHocApp)

    def render(self):
        return u"Hallo WELT"
