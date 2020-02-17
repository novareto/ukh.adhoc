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
def handle_save(obj, event, transition='publish'):

    #####################################################
    #
    # Wie komme ich hier an die Grunddaten ????
    # 
    # Ich benötige die Mailadresse des versicherten (und Name etc.)
    #
    # Meine Versuche wi z.B
    #
    # grunddaten = IAccountData(obj.__parent__)
    #
    # sind fehlgeschlagen...
    #
    #####################################################
    #import pdb; pdb.set_trace()
    sp = transaction.savepoint()
    try:
        betreff = obj.title
        nachrichtentext = obj.message
        fname = None
        filename = None
        adrz1 = "NN"
        adrz2 = "NN"
        adrz3 = "NN"
        #if hasattr(obj.attachment, 'data'):
        #    ntf = tempfile.NamedTemporaryFile()
        #    ntf.write(obj.attachment.data)
        #    ntf.seek(0)
        #    fname = ntf.name
        #    filename = obj.attachment.filename
        #um = getUtility(IUserManagement)
        link = "%s?form.field.access_token=%s" % (grok.url(event.request, obj, 'add'), make_token())
        #link = link.replace('https://schule-login.ukh.de', 'http://10.64.54.12:7787/app')
        f_adr = "extranet@ukh.de"
        #hf = getHomeFolder(obj)
        ## Servicetelefon !!!!
        #if event.principal.id == "servicetelefon-0":
        #    f_adr = "ukh@ukh.de"
        #    body = BODYR % (nachrichtentext)
        #    antwortto = um.getUser(hf.__name__).get('email').strip()
        #    to = [antwortto, ]
        ## Schule
        ##if event.principal.id != "servicetelefon-0":
        #else:
        #    to = ['ukh@ukh.de', ]
        #    sdat = event.principal.getAdresse()
        #    adrz1 = sdat['iknam1'].strip() + ' ' + sdat['iknam2'].strip()
        #    adrz2 = sdat['ikstr'].strip()### + ' ' + sdat['iknam2'].strip()
        #    adrz3 = str(sdat['enrplz']).strip() + ' ' + sdat['ikhort'].strip()
        #    body = BODY % (adrz1, adrz2, adrz3, nachrichtentext, link)
        body = BODY % (adrz1, adrz2, adrz3, nachrichtentext, link)
        to = ['m.seibert@ukh.de', ]
        #filename = remove_accents(filename)
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
