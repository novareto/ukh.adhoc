# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import json
import functools

import zope.component
import zope.schema
from zope.interface.exceptions import BrokenImplementation
from zope.interface.verify import verifyObject

from .serialize import fields


def validate(data, fields, strict=True):
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
            errors.append('Missing field `%s`' % name)
    if data:
        errors.append('Unexpected field `%s`' % ', '.join(data.keys()))
    return parsed, errors


def expected(*fields, **kws):
    strict = kws.get('strict', True)
    decode = kws.get('decode', json.loads)

    def method_validator(api_meth):

        @functools.wraps(api_meth)
        def validate_incoming_data(api):
            data = decode(api.body)
            parsed, errors = validate(data, fields, strict)
            return api_meth(api, parsed, errors)
        return validate_incoming_data

    return method_validator
