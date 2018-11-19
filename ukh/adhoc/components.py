# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok

from ukh.adhoc import IAccount
from zope.interface import implementer


@implementer(IAccount)
class Account(grok.Container):
    def __init__(self, az, password, mail, oid, actions, document_information):
        self.az = az
        self.password = password
        self.mail = mail
        self.oid = oid
        self.actions = actions
        self.id = az
        self.document_information = document_information

    def checkPassword(self, password):
        return True
