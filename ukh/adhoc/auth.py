# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import grok
import base64
import urllib
import uvcsite

from ukh.adhoc.components import Account
from uvcsite import log
from uvc.tbskin.skin import ITBSkinLayer
from zope.pluggableauth import factories
from zope.pluggableauth import interfaces
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.component import getUtility
from zope.location.location import located
from zope.interface import implementer
from zope.pluggableauth.interfaces import IPrincipalInfo
from dolmen.app.authentication.browser.login import ILoginForm, Login
from dolmen.app.authentication.plugins.cookies import CookiesCredentials
from zope import schema
from zope.session.interfaces import ISession
from zope.publisher.interfaces.http import IHTTPRequest


class UKHCookiesCredentials(CookiesCredentials):
    grok.name("ukh_cookies")

    gebdatefield = "gebdate"

    @staticmethod
    def make_cookie(login, password, gebdate):
        credstr = u"%s:%s:%s" % (login, password, gebdate)
        val = base64.encodestring(credstr.encode("utf-8"))
        return urllib.quote(val)

    def extractCredentials(self, request):
        if not IHTTPRequest.providedBy(request):
            return

        login = request.get(self.loginfield, None)
        password = request.get(self.passwordfield, None)
        gebdate = request.get(self.gebdatefield, None)
        cookie = request.get(self.cookie_name, None)

        if login and password and gebdate:
            cookie = self.make_cookie(login, password, gebdate)
            request.response.setCookie(self.cookie_name, cookie, path="/")
        elif cookie:
            val = base64.decodestring(urllib.unquote(cookie)).decode("utf-8")
            login, password, gebdate = val.split(":")
        else:
            return
        return {"login": login, "password": password, "gebdate": gebdate}


class IUKHLoginForm(ILoginForm):

    gebdate = schema.TextLine(
        title=u"Geburtsdatum",
        description=u"",
        required=True
    )


class Login(Login):
    grok.layer(ITBSkinLayer)

    @property
    def fields(self):
        fields = uvcsite.Fields(IUKHLoginForm)
        fields["gebdate"].htmlAttributes["placeholder"] = u"TT.MM.JJJJ"
        for field in fields:
            field.prefix = u""
        return fields


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
            raise KeyError("Account `%s` already exists." % account.az)
        self._users[account.az] = account
        log("Successfully Created User %s" % account.az)
        return True

    def delete(self, key):
        if key in self._users:
            del self._users[key]
            return True
        return False

    def update(self, key, **data):
        user = self.get(key)
        if user is None:
            raise KeyError("Account `%s` does not exist." % key)
        for field, value in data.items():
            setattr(user, field, value)
        return True


@implementer(IAuthenticatorPlugin)
class UserAuthenticatorPlugin(UsersManagement, grok.LocalUtility):
    grok.name("users")

    def authenticateCredentials(self, credentials):
        USER_SESSION_KEY = "adhoc.authentication"
        request = uvcsite.getRequest()
        session = ISession(request)['adhoc.authentication']
        authenticated = session.get(USER_SESSION_KEY)
        if authenticated is None:
            if not isinstance(credentials, dict):
                return
            account = self.getAccount(credentials["login"])
            if account is None:
                return None
            if not account.checkPassword(credentials["password"], credentials.get("gebdate", '99.99.9999')):
                return None
            else:
                authenticated = session[USER_SESSION_KEY] = dict(id=account.az)
        return PrincipalInfo(**authenticated)

    def getAccount(self, login):
        return self.get(login)

    def principalInfo(self, id):
        account = self.getAccount(id)
        if account is None:
            return
        return PrincipalInfo(id=account.az)


def get_account(name):
    util = getUtility(IAuthenticatorPlugin, "users")
    account = util.getAccount(name)
    if account is not None:
        located(account, grok.getSite(), name)
    return account


class AdHocPrincipal(factories.Principal, Account):
    info = "CUSTOM PROPERTY"

    def __repr__(self):
        return "Principal('%s')" % self.id

from .interfaces import IUKHAdHocLayer
from zope.interface import alsoProvides
class AdHocPrincipalFactory(factories.AuthenticatedPrincipalFactory, grok.MultiAdapter):
    grok.adapts(interfaces.IPrincipalInfo, ITBSkinLayer)
    #grok.baseclass()

    def __call__(self, authentication):
        principal = super(AdHocPrincipalFactory, self).__call__(authentication)
        #principal = AdHocPrincipal(
        #    authentication.prefix + self.info.id, self.info.description
        #)
        #grok.notify(
        #    interfaces.AuthenticatedPrincipalCreated(
        #        authentication, principal, self.info, self.request
        #    )
        #)
        alsoProvides(self.request, IUKHAdHocLayer)
        return principal


from ukh.adhoc.interfaces import IUKHAdHocApp
from dolmen.authentication import UserLoginEvent
class CheckRemote(grok.XMLRPC):
    grok.context(IUKHAdHocApp)

    def checkAuth(self, user, password, gebdate):
        plugin = getUtility(IAuthenticatorPlugin, 'users')
        principal = plugin.authenticateCredentials(dict(
            login=user,
            password=password,
            gebdate=gebdate))
        if principal:
            grok.notify(UserLoginEvent(factories.Principal(user)))
            return 1
        return 0
