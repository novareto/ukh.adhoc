# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import pytz
import grok
import transaction

import zope.component
import zope.schema


from base64 import decodestring
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from .components import Account, Document
from .interfaces import IAccount, IDocumentInfo, IUKHAdHocApp
from .interfaces import IMessage, IQuestion, IAnswer
from .lib.serialize import serialize, fields
from .lib.validate import expected, error_handler
from uvc.letterbasket.components import Message
from uvcsite.utils.mail import send_mail
from zope.interface import directlyProvides
from hurry.workflow.interfaces import IWorkflowState, IWorkflowInfo
from uvc.layout.forms.event import AfterSaveEvent


tz = pytz.timezone("Europe/Berlin")


BODY = u"""\
Guten Tag,

in Ihrem Versichertenportal wartet eine neue Nachricht auf Sie.

Um die Nachricht zu lesen, melden Sie sich bitte in Ihrem Versichertenportal \
der Unfallkasse Hessen auf www.ukh.de/versichertenportal an.


Freundliche Grüße
Ihre Unfallkasse Hessen


Diese E-Mail-Nachricht wurde von einer ausschließlichen Benachrichtungsadresse versandt,\
die keine eingehenden Nachrichten empfängt. Bitte antworten Sie nicht auf diese E-Mail-Nachricht.
"""


#ETEXT1 = u"""
#Guten Tag,
#
#wir freuen uns, dass Sie sich für das Versichertenportal entschieden haben.
#
#Damit können Sie Anfragen schnell und einfach online beantworten.
#
#Wahrscheinlich ist unsere Anfrage vom %s im Alltag in Vergessenheit geraten, deshalb möchten wir Sie mit
#dieser Nachricht gerne an die Erledigung erinnern.
#
#Die Anfrage finden Sie im Bereich Formulare. Vielen Dank für Ihre Mithilfe.
#
#Freundliche Grüße
#
#Ihre Unfallkasse Hessen
#"""
#
#ETEXT2 = u"""
#Guten Tag,
#
#unsere Anfrage vom %s wurde von Ihnen bisher noch nicht beantwortet.
#
#Wir erinnern Sie hiermit an die Erledigung. Etwaige Hinderungsgründe bitten wir uns mitzuteilen.
#
#Wir sind gesetzlich verpflichtet, Sie auf Ihre bestehenden Mitwirkungspflichten hinzuweisen.
#Diese ergeben sich aus den §§ 60 ff. Sozialgesetzbuch-Allgemeiner Teil (SGB I).
#Hiernach müssen Sie dem gesetzlichen Unfallversicherungsträger die notwendigen Angaben machen.
#
#Bei fehlender Mitwirkung können Leistungen (Geld-und Sachleistungen) ganz oder teilweise
#versagt oder entzogen werden (§ 66 SGB I).
#
#Die Anfrage finden Sie im Bereich Formulare.
#
#Freundliche Grüße
#
#Ihre Unfallkasse Hessen
#"""


class AdHocService(grok.JSON):
    grok.context(IUKHAdHocApp)

    @property
    def manager(self):
        return zope.component.getUtility(
            IAuthenticatorPlugin, name="users")

    @expected(*fields(IAccount), strict={'az'})
    @error_handler
    def add(self, data):
        account = Account(**data)
        self.manager.add(account)
        self.request.response.setStatus(201)
        return

    @expected(*fields(IAccount), strict={'az'})
    @error_handler
    def update(self, data):
        key = data.pop('az')
        if data:
            self.manager.update(key, **data)
            self.request.response.setStatus(202)
            return
        raise KeyError('No fields to update.')

    @expected(IAccount['az'])
    @error_handler
    def get(self, data):
        user = self.manager.get(data['az'])
        if user is not None:
            struct = serialize(user, IAccount)
            return struct._asdict()
        raise KeyError('Unknown user.')

    @expected(IAccount['az'])
    @error_handler
    def get_user(self, data):
        user = self.manager.get(data['az'])
        if user is not None:
            docs = []
            for name, obj in user.items():
                if name != 'nachrichten':
                    docs.append(dict(doc_id=name, doc_type=obj.doc_type, status=obj.state, date=obj.modtime.astimezone(tz).strftime('%d.%m.%Y')))
            struct = dict(az=user.az, password=user.password, email=user.email, docs=docs,
                          active=user.active, anfragedatum=user.anfragedatum, status=user.status)
            return struct
        raise KeyError('Unknown user !!!.')

    @expected(IAccount['az'], *fields(IDocumentInfo))
    @error_handler
    def submit_document(self, data):
        user = self.manager.get(data['az'])
        if user is not None:
            info = data.by_schema[IDocumentInfo]
            view = zope.component.getMultiAdapter(
                (self.context, self.request), name=data.get('doc_type'))
            defaults = data.pop('defaults')
            data.update(defaults)
            doc = view.create(data)
            if not doc:
                doc = Document(**info)
            name = user.add(data.get('doc_type'), doc)
            self.request.response.setStatus(202)
            return {'id': name}
        raise KeyError('Unknown user.')

    #@expected(IAccount['az'], *fields(IDocumentInfo))
    #@error_handler
    #def submit_notification(self, data):
    #    user = self.manager.get(data['az'])
    #    ETEXT = ''
    #    if user is not None:
    #        anfragedatum = data.get('anschreiben')[1:11]
    #        # info = data.by_schema[IDocumentInfo]
    #        # document = user[data.get('doc_type')]
    #        if data.get('anschreiben')[0] == '1':
    #            ETEXT = ETEXT1 % (anfragedatum)
    #            BETREFF = u'Erinnerung'
    #        if data.get('anschreiben')[0] == '2':
    #            ETEXT = ETEXT2 % (anfragedatum)
    #            BETREFF = u'2. Erinnerung mit Hinweis auf Mitwirkungspflicht'
    #        send_mail('versichertenportal@ukh.de', [user.email, ], BETREFF, ETEXT)

    @expected(IAccount['az'], *fields(IMessage, select=('doc_id', 'message', 'title', 'attachment', 'filename', 'sachbearbeiter')), strict=('title', 'message'))
    @error_handler
    def submit_letter(self, data):
        account = self.manager.get(data['az'])
        user = self.manager.get(data['az'])
        if user is not None:
            info = data.by_schema[IMessage]
            message = Message()
            grok.notify(grok.ObjectCreatedEvent(message))
            from dolmen.forms.base import set_fields_data
            if 'attachment' in info.keys():
                from StringIO import StringIO
                f = StringIO(decodestring(info['attachment']))
                # f.filename="download"
                f.filename = info['filename']
                info['attachment'] = f
            set_fields_data(IMessage, message, info)
            directlyProvides(message, IQuestion)
            user['nachrichten'].add(message)
            grok.notify(AfterSaveEvent(message, self.request))
            self.request.response.setStatus(202)
            return
        raise KeyError('Unknown user.')

    @expected(IAccount['az'], *fields(IMessage, select=('doc_id', 'message', 'title', 'attachment', 'filename', 'sachbearbeiter')), strict=('title', 'message', 'doc_id'))
    @error_handler
    def reply_letter(self, data):
        account = self.manager.get(data['az'])
        user = self.manager.get(data['az'])
        if user is not None:
            info = data.by_schema[IMessage]
            message = Message()
            grok.notify(grok.ObjectCreatedEvent(message))
            from dolmen.forms.base import set_fields_data
            if 'attachment' in info.keys():
                from StringIO import StringIO
                f = StringIO(decodestring(info['attachment']))
                # f.filename="download"
                f.filename = info['filename']
                info['attachment'] = f
            set_fields_data(IMessage, message, info)
            directlyProvides(message, IAnswer)
            user['nachrichten'][info['doc_id']].add(message)
            print "I ADDED A MESSAGE"
            # with transaction.manager as t:
            #     print t
            grok.notify(AfterSaveEvent(message, self.request))
            #import pdb; pdb.set_trace()
            #IWorkflowInfo(message).fireTransition('finish')
            self.request.response.setStatus(202)
            return
        raise KeyError('Unknown user.')

    @expected(IAccount['az'])
    @error_handler
    def list_documents(self, data):
        user = self.manager.get(data['az'])
        if user is not None:
            docs = []
            for message in user['nachrichten'].values():
                an = {}
                answer = [x for x in message.values()]
                if len(answer) == 1:
                    answer = answer[0]
                    an = dict(
                        date=answer.modtime.astimezone(tz).strftime('%d.%m.%Y %H:%M'),
                        author=answer.principal.id,
                        az=answer.__name__,
                        doc_id=answer.__name__,
                        wf_state=IWorkflowState(answer).getState().value,
                        message=answer.message,
                        title=answer.title
                    )
                docs.append(
                    dict(
                        date=message.modtime.astimezone(tz).strftime('%d.%m.%Y %H:%M'),
                        author=message.principal.id,
                        az=user.__name__,
                        doc_id=message.__name__,
                        wf_state=IWorkflowState(message).getState().value,
                        message=message.message,
                        title=message.title,
                        answer = an
                    )
                )
            print docs
            return docs
        raise KeyError('Unknown user.')
