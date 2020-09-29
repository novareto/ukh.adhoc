#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grok
import uvcsite
import tempfile
import transaction

from grokcore.message import send
from uvc.letterbasket.interfaces import IMessage
from uvcsite.utils.mail import send_mail
from hurry.workflow.interfaces import IWorkflowInfo
from ukh.adhoc.interfaces import IAccountData
from ukh.adhoc.stammdaten import PRStatistik
from uvc.token_auth.plugin import TokenAuthenticationPlugin
from pdf import Nachricht_pdf
from ..event import MES
from ukh.adhoc.interfaces import IQuestion, IAnswer


def getAccount(obj):
    if IQuestion.providedBy(obj):
        account = obj.__parent__.__parent__
    elif IAnswer.providedBy(obj):
        account = obj.__parent__.__parent__.__parent__
    return account


@grok.subscribe(IMessage, uvcsite.IAfterSaveEvent)
def handle_save(obj, event, transition='sent'):
    sp = transaction.savepoint()
    account = getAccount(obj)
    try:
        if obj.principal.id == 'zope.anybody':
            email = account.email
            message = MES
            send_mail(
                "versichertenportal@ukh.de",
                [email],
                "Sie haben neue Nachrichten!",
                message,
            )
        else:
            grunddaten = account.getGrundDaten()
            nname = grunddaten['iknam1'].strip()
            vname = grunddaten['iknam2'].strip()
            PRStatistik(obj.principal.id, 'ENachricht', '004050')
            Nachricht_pdf(obj, nname, vname, tmp=None)
            send(u'Vielen Dank, Ihre Nachricht wurde gesendet.')
        IWorkflowInfo(obj).fireTransition(transition)
    except StandardError as exc:
        uvcsite.logger.exception("Achtung FEHLER")
        sp.rollback()
        IWorkflowInfo(obj).fireTransition('progress')
