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

from .interfaces import IAccount, IUKHAdHocApp
from .components import Account


def fields(*schemas):
    for schema in schemas:
        for name, field in zope.schema.getFieldsInOrder(schema):
            yield field


def serialize(obj, *schemas):
    all_fields = {f.__name__: f for f in fields(*schemas)}
    values = {}
    representation = namedtuple(
        obj.__class__.__name__, list(all_fields.keys()))

    for name, field in all_fields.items():
        values[name] = field.bind(obj).get(obj)
    return representation(**values)


def expected(*fields, **kws):

    strict = kws.get('strict', True)

    def method_validator(api_meth):
        @functools.wraps(api_meth)
        def validate_incoming_json(api):
            data = json.loads(api.body)
            parsed = {}
            errors = []
            for field in fields:
                name = field.__name__
                if name in data:
                    value = data.pop(name)
                    try:
                        field.validate(value)
                    except zope.schema.ValidationError as err:
                        errors.append('%s: %s' % (name, err.__doc__))
                    else:
                        parsed[name] = value
                elif field.required and (strict is True or name in strict):
                    import pdb
                    pdb.set_trace()
                    errors.append('Missing field `%s`' % name)
            if data:
                errors.append('Unexpected field `%s`' % ', '.join(data.keys()))
            return api_meth(api, parsed, errors)

        return validate_incoming_json
    return method_validator


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
