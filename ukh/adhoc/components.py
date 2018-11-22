# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
from persistent import Persistent
from persistent.list import PersistentList
from zope.interface import implementer
from ukh.adhoc.interfaces import IAccount, IDocumentInfo


@implementer(IAccount)
class Account(grok.Container):

    def __init__(self, az, password, email, oid):
        super(Account, self).__init__()
        self.az = az
        self.password = password
        self.email = email
        self.oid = oid
        self.id = az
        self.documents = PersistentList()

    def checkPassword(self, password):
        return True


@implementer(IDocumentInfo)
class Document(Persistent):
    doc_type = None
    defaults = None

    def __init__(self, doc_type, defaults):
        super(Document, self).__init__()
        self.doc_type = doc_type
        self.defaults = defaults
