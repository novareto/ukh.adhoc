# -*- coding: utf-8 -*-

import zope.schema
from collections import namedtuple


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
