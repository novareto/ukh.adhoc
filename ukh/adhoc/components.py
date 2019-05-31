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

    def __init__(self, az, password, email, oid, ansprechpartner, anrede, active):
        super(Account, self).__init__()
        self.az = az
        self.password = password
        self.email = email
        self.oid = oid
        self.id = az
        self.ansprechpartner = ansprechpartner
        self.anrede = anrede
        self.active = active

    def checkPassword(self, password):
        return True


from uvc.adhoc.components import AdHocContent
from hurry.workflow.interfaces import IWorkflowState

class UKHAdHocContent(AdHocContent):

    @property
    def doc_title(self):
        return grok.title.bind().get(self)

    @property
    def doc_name(self):
        return grok.name.bind().get(self)

    @property
    def state(self):
        from uvcsite.workflow.basic_workflow import titleForState
        return titleForState(IWorkflowState(self).getState())



@implementer(IDocumentInfo)
class Document(Persistent):
    doc_type = None
    defaults = None

    def __init__(self, doc_type, defaults):
        super(Document, self).__init__()
        self.doc_type = doc_type
        self.defaults = defaults
