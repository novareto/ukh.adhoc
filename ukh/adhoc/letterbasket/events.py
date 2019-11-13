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
from uvc.letterbasket.auth import make_token



@grok.subscribe(IMessage, uvcsite.IAfterSaveEvent)
def handle_save(obj, event, transition='publish'):
    sp = transaction.savepoint()
    try:
        betreff = obj.title
        nachrichtentext = obj.message
        to = ['m.seibert@ukh.de', 'ck@novareto.de']
        f_adr = "schulportal@ukh.de"
        body = "NEUE NACHRICHT"
        link = "%s?form.field.access_token=%s" % (grok.url(event.request, obj, 'add'), make_token())
        send_mail(
            f_adr,
            to,
            "BETREFF",
            body=body + link
        )

        IWorkflowInfo(obj).fireTransition(transition)
    except StandardError:
        sp.rollback()
        IWorkflowInfo(obj).fireTransition('progress')
        uvcsite.logger.exception("Achtung FEHLER")
