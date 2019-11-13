# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# cklinger@novareto.de

import grok
import datetime

from uvcsite.utils.mail import send_mail
from uvc.adhoc.interfaces import IAdHocContent
from ukh.adhoc.interfaces import IAccountData


MES = u"""
Die Unfallkasse Hessen hat Ihnen im Rahmen des elektronischen Verfahrens am %s
folgende Fragebogen / folgende Fragebögen gesendet:

%s

Wir bitten Sie diesen/diese auszufüllen und an uns zurückzusenden.

Vielen Dank für Ihre Mithilfe.

Freundliche Grüße

Ihre Unfallkasse Hessen
"""


@grok.subscribe(IAdHocContent, grok.IObjectAddedEvent)
def notify_user(obj, event):
    account = obj.__parent__
    grunddaten = IAccountData(obj.__parent__)
    message = MES % (datetime.datetime.now().strftime('%d.%m.%Y'), obj.doc_title)
    #send_mail('extranet@ukh.de', ['m.seibert@ukh.de', 'ck@novareto.de'], 'Sie haben neue Nachrichten!', message)
    send_mail('extranet@ukh.de', [grunddaten.email, ], 'Sie haben neue Nachrichten!', message)
