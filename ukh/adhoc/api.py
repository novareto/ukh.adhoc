# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import json
import grok
import functools
from collections import namedtuple

import zope.component
import zope.schema
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from .serialize import serialize, fields
from .validate import expected, error_handler
from .interfaces import IAccount, IDocumentInfo, IUKHAdHocApp
from .components import Account, Document
from zeam.form.base.components import Collection
from zope.interface.interfaces import IInterface
from uvc.letterbasket.components import Message
from uvc.letterbasket.interfaces import IMessage, IThreadRoot
from zope.interface import directlyProvides



class AdHocService(grok.JSON):
    grok.context(IUKHAdHocApp)

    @property
    def manager(self):
        return zope.component.getUtility(
            IAuthenticatorPlugin, name="users")

    @expected(*fields(IAccount), strict={'az'})
    #@expected(*Fields(IAccount).select('az'))
    @error_handler
    def add(self, data):
        #import pdb; pdb.set_trace()
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


    @expected(IAccount['az'], *fields(IMessage))
    @error_handler
    def submit_letter(self, data):
        user = self.manager.get(data['az'])
        if user is not None:
            info = data.by_schema[IMessage]
            message = Message()
            from dolmen.forms.base import set_fields_data
            set_fields_data(IMessage, message, info)
            directlyProvides(message, IThreadRoot)
            user['nachrichten'].add(message)
            self.request.response.setStatus(202)
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
