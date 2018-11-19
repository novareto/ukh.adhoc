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
from .interfaces import IAccount, IUKHAdHocApp
from .components import Account


class AdHocService(grok.JSON):
    grok.context(IUKHAdHocApp)

    @property
    def manager(self):
        return zope.component.getUtility(
            IAuthenticatorPlugin, name="users")

    @expected(*fields(IAccount))
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
