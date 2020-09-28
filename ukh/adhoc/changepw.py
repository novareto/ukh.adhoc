# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


import grok

from zope.component import getUtility
from uvcsite.utils.mail import send_mail
from .interfaces import IUKHAdHocApp


TEXT = u"""
Guten Tag,

bitte öffnen Sie nachfolgenden Link um Ihr Passwort zurückzusetzen und ein neues Passwort zu vergeben.

https://versichert.ukh.de/login/resetpassword?form.field.username=%s&form.field.challenge=%s

Sie haben kein neues Passwort angefordert? In diesem Fall ignorieren Sie diese Email.


Ihre Unfallkasse Hessen
"""


TEXT_CONFIRM = u"""
Guten Tag,

kürzlich wurde das Passwort für Ihren Zugang zum Versichertenportal geändert.
Benutzername: %s

Wenn Sie diese Passwortänderung nicht angefordert haben, wenden Sie sich bitte an unser Servicetelefon unter 069 29972-440.
(Montags bis Freitags von 7:30 bis 18:00 Uhr)

E-Mail: ukh@ukh.de


Ihre Unfallkasse Hessen

"""


def getUser(az):
    from zope.component import getUtility
    from zope.pluggableauth.interfaces import IAuthenticatorPlugin
    pau = getUtility(IAuthenticatorPlugin, 'users')
    account = pau.getAccount(az)
    return account


class PasswordActions(grok.JSON):
    grok.context(IUKHAdHocApp)

    def get_user_base(self):
        mnr = self.request.form.get('username', None)
        if mnr and mnr.isdigit():
            user = getUser(mnr)
            if user:
                #print(dict(mnr=str(user.id), passwort=user.password, email=user.email))
                return dict(mnr=str(user.id), passwort=user.password, email=user.email)
        return {'auth': 0}

    def send_mail(self):
        user = self.request.form.get('username')
        mail = self.request.form.get('email')
        hash = self.request.form.get('hash_value')
        text = TEXT % (user, hash)
        userobject = getUser(user)
        send_mail('versichertenportal@ukh.de', (userobject.email,), u"Versichertenportal Passwortänderung", text)
        return {'success': 'true'}

    def set_user(self):
        username = self.request.form.get('username')
        password = self.request.form.get('password')
        if username and password:
            user = getUser(username)
            user.password = password
            return {'success': 'true'}
        return {'success': 'false'}

    def send_confirm(self):
        user = self.request.form.get('username')
        mail = self.request.form.get('email')
        text = TEXT_CONFIRM % (user)
        userobject = getUser(user)
        send_mail('versichertenportal@ukh.de', (userobject.email,), u"Versichertenportal Passwortänderung", text)
        return {'success': 'true'}

