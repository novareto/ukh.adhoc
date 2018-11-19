# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok

from zope.interface import implementer
from ukh.adhoc.interfaces import IAccount


@implementer(IAccount)
class Account(grok.Container):
    def __init__(self, az, password, mail, oid, document_information=None):
        super(Account, self).__init__()
        self.az = az
        self.password = password
        self.mail = mail
        self.oid = oid
        self.id = az
        self.document_information = document_information

    def checkPassword(self, password):
        return True
