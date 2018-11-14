# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import grok
from zope.pluggableauth.interfaces import IAuthenticatorPlugin, IPrincipalInfo


class PrincipalInfo(object):
    grok.implements(IPrincipalInfo)

    def __init__(self, id):
        self.id = id
        self.title = id
        self.description = id


class UserFolder(grok.Container):
    pass


class UserAuthenticatorPlugin(grok.LocalUtility):
    grok.implements(IAuthenticatorPlugin)
    grok.name("users")

    def __init__(self):
        self.user_folder = UserFolder()

    def authenticateCredentials(self, credentials):
        if not isinstance(credentials, dict):
            return
        account = self.getAccount(credentials["login"])
        if account is None:
            return None
        if not account.checkPassword(credentials["password"]):
            return None
        return PrincipalInfo(id=account.az)

    def getAccount(self, login):
        return login in self.user_folder and self.user_folder[login] or None

    def principalInfo(self, id):
        account = self.getAccount(id)
        if account is None:
            return
        return PrincipalInfo(id=account.az)
