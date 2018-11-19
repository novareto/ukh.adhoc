# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import json
import grok

from zope import component
from ukh.adhoc.interfaces import IUKHAdHocApp
from zope.pluggableauth.interfaces import IAuthenticatorPlugin


class AdHocService(grok.JSON):
    grok.context(IUKHAdHocApp)

    @property
    def users(self):
        auth_util = component.getUtility(IAuthenticatorPlugin, name="users")
        return auth_util.user_folder

    def add(self):
        body = json.loads(self.body)
        return body

    def update(self):
        return {}
