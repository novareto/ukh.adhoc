# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de 

from zope import interface, schema


class IUKHAdHocApp(interface.Interface):
    pass


class IDocumentInfo(interface.Interface):

    doc_type = schema.TextLine(
        title=u"Type of the Document",
        required=True
    )

    defaults = schema.Dict(
        title=u"Default Data",
        required=True,
    )


class IAccount(interface.Interface):

    az = schema.TextLine(
        title=u"Aktenzeichen",
        required=True
    )

    password = schema.Password(
        title=u"Passwort",
        required=True
    )

    email = schema.TextLine(
        title=u"Email",
        required=True
    )

    oid = schema.TextLine(
        title=u"OID Document Number",
        required=True
    )
