# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
from ukh.adhoc.interfaces import IUKHAdHocApp


class AdHocService(grok.JSON):
    grok.context(IUKHAdHocApp)

    def add(self):
        return {}

    def update(self):
        return {}
