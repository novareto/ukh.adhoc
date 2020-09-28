# -*- coding: utf-8 -*-
# Copyright (c) 2007-2019 NovaReto GmbH
# cklinger@novareto.de

import grok
import datetime

from uvcsite.utils.mail import send_mail
from uvc.adhoc.interfaces import IAdHocContent
from ukh.adhoc.interfaces import IAccountData


MES = u"""
Guten Tag,

in Ihrem Versichertenportal wartet eine neue Nachricht auf Sie.

Um die Nachricht zu lesen, melden Sie sich bitte in Ihrem Versichertenportal
der Unfallkasse Hessen auf https://versichert.ukh.de an.


Freundliche Grüße
Ihre Unfallkasse Hessen


Diese E-Mail-Nachricht wurde von einer ausschließlichen Benachrichtungsadresse versandt, \
die keine eingehenden Nachrichten empfängt. Bitte antworten Sie nicht auf diese E-Mail-Nachricht.
"""


@grok.subscribe(IAdHocContent, grok.IObjectAddedEvent)
def notify_user(obj, event):
    if obj.doc_title != "Dateiupload":
        account = obj.__parent__
        grunddaten = IAccountData(obj.__parent__)
        message = MES
        if grunddaten.email.strip() != '':
            send_mail(
                "versichertenportal@ukh.de",
                [grunddaten.email],
                "Sie haben neue Nachrichten!",
                message,
            )
