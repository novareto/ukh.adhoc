# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok


class Account(grok.Model):
    def __init__(self, az, password, mail, oid, actions):
        self.az = az
        self.password = password
        self.mail = mail
        self.oid = oid
        self.actions = actions
        self.id = az

    def checkPassword(self, password):
        return True
