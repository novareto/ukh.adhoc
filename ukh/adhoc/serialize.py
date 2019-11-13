# -*- coding: utf-8 -*-

import zope.schema
from collections import namedtuple


def fields(*schemas, **kw):
    select = kw.get('select')
    for schema in schemas:
        for name, field in zope.schema.getFieldsInOrder(schema):
            if select:
                if name in select:
                    yield field
            else:
                yield field


def serialize(obj, *schemas):
    all_fields = {f.__name__: f for f in fields(*schemas)}
    values = {}
    representation = namedtuple(
        obj.__class__.__name__, list(all_fields.keys()))

    for name, field in all_fields.items():
        values[name] = field.bind(obj).get(obj)
    return representation(**values)
