# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import json
import grok
import functools
from collections import namedtuple

import zope.component
import zope.schema
from zope.interface.exceptions import BrokenImplementation
from zope.interface.verify import verifyObject
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from .serialize import serialize, fields
from .validate import expected
from .interfaces import IAccount, IUKHAdHocApp
from .components import Account


class AdHocService(grok.JSON):
    grok.context(IUKHAdHocApp)

    @property
    def manager(self):
        return zope.component.getUtility(
            IAuthenticatorPlugin, name="users")

    @expected(*fields(IAccount))
    def add(self, data, errors):
        if not errors:
            account = Account(**data)
            try:
                verifyObject(IAccount, account)
            except BrokenImplementation:
                # A bad error occured.
                # This should not happen but could.
                # Please log it.
                self.request.response.setStatus(500)
                return
            try:
                self.manager.add(account)
                self.request.response.setStatus(201)
                return
            except KeyError as err:
                errors.append(err.message)

        self.request.response.setStatus(400)
        return {'errors': errors}
        
    @expected(*fields(IAccount), strict={'az'})
    def update(self, data, errors):
        if not errors:
            try:
                key = data.pop('az')
                if data:
                    self.manager.update(key, **data)
                    self.request.response.setStatus(202)
                    return
                else:
                    # Only az was provided, nothing to update
                    errors.append('No fields to update.')
            except KeyError as err:
                errors.append(err.message)

        self.request.response.setStatus(400)
        return {'errors': errors}

    @expected(IAccount['az'])
    def get(self, data, errors):
        if not errors:
            try:
                user = self.manager[data['az']]
                struct = serialize(user, IAccount)
                return struct._asdict()
            except KeyError as err:
                errors.append('Unknown user.')

        self.request.response.setStatus(400)
        return {'errors': errors}
