# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import grok

import zope.component
import zope.schema


from base64 import decodestring
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from .lib.serialize import serialize, fields
from .lib.validate import expected, error_handler
from .interfaces import IAccount, IDocumentInfo, IUKHAdHocApp
from .components import Account, Document
from uvc.letterbasket.components import Message
from .interfaces import IMessage
from uvc.letterbasket.interfaces import IThreadRoot
from zope.interface import directlyProvides
from uvcsite.utils.mail import send_mail


BODY = u"""\
Guten Tag,

Sie haben eine neue Nachricht!

Bitte melden Sie sich im Versicherten Extranet der Unfallkasse Hessen an und kontrollieren Ihre Nachrichten.


Freundliche Grüße


Unfallkasse Hessen
"""


ETEXT1 = u"""
Die Unfallkasse Hessen hat Ihnen im Rahmen des elektronischen Verfahrens
vor einiger Zeit einen Fragebogen gesendet.

Leider wurde dieser noch nicht bearbeitet.

Wir bitten Sie, sich im Versicherten Extranet anzumelden, den Fragebogen zu bearbeiten und an uns zurückzusenden.

Vielen Dank für Ihre Mithilfe.

Freundliche Grüße

Ihre Unfallkasse Hessen
"""

ETEXT2 = u"""
Die Unfallkasse Hessen hat Ihnen im Rahmen des elektronischen Verfahrens
vor einiger Zeit ein Fragebogen gesendet.

Leider wurde dieser immer noch nicht bearbeitet!

Wir bitten Sie, sich im Versicherten Extranet anzumelden, den Fragebogen zu bearbeiten und an uns zurückzusenden.
Ansonsten sehen wir uns leider gezwungen die Leistungen an Sie einzuschränken.

Vielen Dank für Ihre Mithilfe.

Freundliche Grüße

Ihre Unfallkasse Hessen
"""


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
                    docs.append(dict(doc_type=name, status=obj.state, date=obj.modtime.strftime('%d.%m.%Y')))
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
            user[data.get('doc_type')] = doc
            self.request.response.setStatus(202)
            return
        raise KeyError('Unknown user.')

    @expected(IAccount['az'], *fields(IDocumentInfo))
    @error_handler
    def submit_notification(self, data):
        user = self.manager.get(data['az'])
        ETEXT = ''
        if user is not None:
            # info = data.by_schema[IDocumentInfo]
            # document = user[data.get('doc_type')]
            if data.get('anschreiben') == '1':
                ETEXT = ETEXT1
            if data.get('anschreiben') == '2':
                ETEXT = ETEXT2
            send_mail('extranet@ukh.de', [user.email, ], 'Erinnerung!', ETEXT)

    @expected(IAccount['az'], *fields(IMessage))
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
            directlyProvides(message, IThreadRoot)
            user['nachrichten'].add(message)
            self.request.response.setStatus(202)
            to = [account.email]
            body = BODY
            f_adr = "extranet@ukh.de"
            send_mail(
                f_adr,
                to,
                u"Neue Nachricht",
                body=body,
            )
            return
        raise KeyError('Unknown user.')

    @expected(IAccount['az'])
    @error_handler
    def list_documents(self, data):
        user = self.manager.get(data['az'])
        if user is not None:
            docs = [
                serialize(doc, IDocumentInfo)._asdict()
                for doc in user.documents]
            return docs
        raise KeyError('Unknown user.')
