# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import grok
from zope.interface import implementer
from zope.pluggableauth.interfaces import IAuthenticatorPlugin, IPrincipalInfo

from .interfaces import IAccount


@implementer(IPrincipalInfo)
class PrincipalInfo:

    def __init__(self, id):
        self.id = id
        self.title = id
        self.description = id


class UsersFolder(grok.Container):
    pass


class UsersManagement:

    def __init__(self):
        self._users = UsersFolder()

    def __getitem__(self, key):
        return self._users[key]

    def get(self, key):
        return self._users.get(key)

    def add(self, account):
        if account.az in self._users:
            raise KeyError('Account `%s` already exists.' % account.az)
        self._users[account.az] = account
        return True

    def delete(self, key):
        if key in self._users:
            del self._users[key]
            return True
        return False

    def update(self, key, **data):
        user = self.get(key)
        if user is None:
            raise KeyError('Account `%s` does not exist.' % key)
        for field, value in data.items():
            setattr(user, field, value)
        return True


@implementer(IAuthenticatorPlugin)
class UserAuthenticatorPlugin(UsersManagement, grok.LocalUtility):
    grok.name("users")

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
        return self.get(login)

    def principalInfo(self, id):
        account = self.getAccount(id)
        if account is None:
            return
        return PrincipalInfo(id=account.az)
