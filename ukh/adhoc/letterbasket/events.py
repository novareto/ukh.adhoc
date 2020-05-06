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
from ukh.adhoc.interfaces import IAccountData


BODY = u"""\
Guten Tag,

die Versicherte Person:

%s

%s
%s


hat folgendes Anliegen:

%s

Antworten Sie bitte mit diesem Link: %s

Gegebenenfalls koennen Sie die Mail auch an den entsprechenden Sachbearbeiter weiterleiten.



Vielen Dank

Ihr Versicherten Extranet
"""


@grok.subscribe(IMessage, uvcsite.IAfterSaveEvent)
def handle_save(obj, event, transition='sent'):
    import pdb; pdb.set_trace()
    sp = transaction.savepoint()
    try:
        betreff = obj.title
        nachrichtentext = obj.message
        fname = None
        filename = None
        adrz1 = "NN"
        adrz2 = "NN"
        adrz3 = "NN"
        link = "%s?form.field.access_token=%s" % (grok.url(event.request, obj, 'add'), make_token())
        f_adr = "extranet@ukh.de"
        body = BODY % (adrz1, adrz2, adrz3, nachrichtentext, link)
        to = ['m.seibert@ukh.de', ]
        send_mail(
            f_adr,
            to,
            u"Anfrage TEST %s" % betreff,
            #u"Anfrage Schulportal: " + str(betreff),
            body=body,
            file=fname,
            filename=filename
        )
        IWorkflowInfo(obj).fireTransition(transition)
        send(u'Vielen Dank, Ihre Nachricht wurde gesendet.', type='message', name='session')
    except StandardError:
        sp.rollback()
        IWorkflowInfo(obj).fireTransition('progress')
        uvcsite.logger.exception("Achtung FEHLER")


#@grok.subscribe(IMessage, uvcsite.IAfterSaveEvent)
#def handle_save(obj, event, transition='publish'):
#    sp = transaction.savepoint()
#    try:
#        betreff = obj.title
#        nachrichtentext = obj.message
#        #to = ['m.seibert@ukh.de', 'ck@novareto.de']
#        to = ['m.seibert@ukh.de',]
#        f_adr = "schulportal@ukh.de"
#        body = "NEUE NACHRICHT"
#        link = "%s?form.field.access_token=%s" % (grok.url(event.request, obj, 'add'), make_token())
#        send_mail(
#            f_adr,
#            to,
#            "BETREFF",
#            body=body + link
#        )
#
#        IWorkflowInfo(obj).fireTransition(transition)
#    except StandardError:
#        sp.rollback()
#        IWorkflowInfo(obj).fireTransition('progress')
#        uvcsite.logger.exception("Achtung FEHLER")
