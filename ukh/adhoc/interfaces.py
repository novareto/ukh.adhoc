# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import grok
import uvcsite 
from zope import interface, schema
from grokcore.component import provider

from zope.schema.interfaces import IContextSourceBinder, IBaseVocabulary
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from ukhtheme.grok.layout import ISkin

class IAdHocContent(uvcsite.IContent):
    """ Marker Interface for AdHoc Content Types
    """
    title = schema.TextLine(
        title = u"Titel",
        description = u"",
        readonly = True,
        required = True)

    docid = schema.TextLine(title=u'docid')

    doc_type = schema.TextLine(
        title=u"Type of the Document",
        required=True
    )

    anschreiben = schema.Text(
        title=u"Anschreiben",
        required=False,
    )


class IUKHAdHocLayer(grok.IDefaultBrowserLayer):
    """MarkerInterface"""


class IAdHocSkin(IUKHAdHocLayer, ISkin):
    grok.skin('ukhtheme_adhoc')



#@provider(IContextSourceBinder)
#def source_active(context):
#    return SimpleVocabulary([
#        SimpleTerm('ja', 'ja', u'Ja, ich möchte am elektronischen Verfahren teilnehmen'),
#        SimpleTerm('nein', 'nein', u'Nein, ich möchte weiterhin auf dem Postweg mit Ihnen kommunizieren')
#    ])
#
#
#@provider(IBaseVocabulary)
#def source_anrede(context):
#    return SimpleVocabulary([
#        SimpleTerm('1', 'Frau', u'Frau'),
#        SimpleTerm('2', 'Herr', u'Herr'),
#        SimpleTerm('3', 'Divers', u'Divers')
#    ])


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

    anschreiben = schema.Text(
        title=u"Anschreiben",
        required=False,
    )

    aktz = schema.TextLine(
        title=u"Aktenzeichen",
        required=True
    )


class IAccount(interface.Interface):

    az = schema.TextLine(
        title=u"Aktenzeichen",
        required=True
    )

    sb_name = schema.TextLine(
        title=u"Sachbearbeiter Name UKH",
        required = False
    )

    sb_mail = schema.TextLine(
        title=u"Sachbearbeiter Mail UKH",
        required = False
    )

    passworda = schema.Password(
        title=u"Bitte tragen Sie hier ihr altes Passwort ein.",
        required=True
    )

    password = schema.Password(
        title=u"Bitte tragen Sie hier ihr neues Passwort ein.",
        required=True
    )

    passwordv = schema.Password(
        title=u"Bitte bestätigen Sie das neue Passwort.",
        required=True
    )

    email = schema.TextLine(
        title=u"E-Mail*",
        description=u"Für die zukünftige Kommunikation benötigen wir Ihre E-Mail Adresse:",
        required=True
    )

    email2 = schema.TextLine(
        title=u"E-Mail Wiederholung*",
        description=u"Bitte bestätigen Sie Ihre E-Mail Adresse:",
        required=True
    )

    oid = schema.TextLine(
        title=u"OID Document Number",
        required=True
    )

    active = schema.Choice(
        title=u"Teilnahme",
        description=u"Wollen sie am Verfahren teilnehmen",
        values=(u'ja', u'nein'),
    )

    datenerhebung = schema.Choice(
        title=u"Einwilligung zur Datenerhebung",
        description=u"Hiermit bestätige ich die oben genannten Dokument der\
            UKH gelesen und akzeptiert zu haben.",
        values=(u'ja', u'nein'),
        required=True
    )

    datenuebermittlung = schema.Choice(
        title=u"Einwilligung zur Datenübermittlung",
        description=u"Hiermit bestätige ich die oben genannten Dokument der\
            UKH gelesen und akzeptiert zu haben.",
        values=(u'ja', u'nein'),
        required=True
    )

    anfragedatum = schema.TextLine(
        title=u"Anfragedatum",
        description=u"Anfragedatum"
    )

    status = schema.TextLine(
        title=u"Status Anfrage",
        description=u"Status Anfrage",
        required=False
    )

    ansprechpartner = schema.TextLine(
        title=u"Ansprechpartner",
        description=u"Ansprechpartner"
    )

    telefon = schema.TextLine(
        title=u"Telefon",
        description=u"Telefon"
    )

    anrede = schema.Choice(
        title=u"Geschlecht",
        values=(u'Frau', u'Herr', u'Divers')
    )

    nname = schema.TextLine(
        title=u"Nachname"
    )

    vname = schema.TextLine(
        title=u"Vorname"
    )

    # Adresse (sollte aus der Datenbank kommen)
    vsstr = schema.TextLine(
        title=u"Straße"
    )

    vshnr = schema.TextLine(
        title=u"Hausnummer",
        required=False
    )

    vsplz = schema.TextLine(
        title=u"Postleitzahl"
    )

    vsort = schema.TextLine(
        title=u"Ort"
    )

    gebdat = schema.TextLine(
        title=u"Geburtsdatum *",
        required=False
    )

    unfdat = schema.TextLine(
        title=u"Unfalldatum",
        required=False
    )

    unfzeit = schema.TextLine(
        title=u"Unfallzeit",
        required=False
    )

    vsvwl = schema.TextLine(
        title=u"Vorwahl",
        required=False
    )

    vstel = schema.TextLine(
        title=u"Telefonnummer",
        required=False
    )

    handy = schema.TextLine(
        title=u"Handy / Mobilfunknummer",
        required=False
    )

    jobinfo1 = schema.TextLine(
        title=u"Arbeitgeber*in oder Unfallbetrieb *",
        description=u"Bitte genauen Namen und Anschrift.",
        required=True
    )

    jobinfo2 = schema.TextLine(
        title=u"Berufliche Tätigkeit oder unfallbringende Tätigkeit *",
        description=u"",
        required=True
    )

    kkdaten = schema.TextLine(
        title=u"Krankenkasse *",
        description=u"Bitte genauen Namen, Anschrift und Versichertennummer.",
        required=True
    )

    hausarzt = schema.TextLine(
        title=u"Hausarzt / Hausärztin *",
        description=u"Bitte genauen Namen und Anschrift.",
        required=True
    )


class IAccountData(IAccount):
    pass


from zope.location.interfaces import IContained
from zope.container.interfaces import IContainer
from zope.container.constraints import contains
from dolmen.file import FileField
from uvc.letterbasket.interfaces import IThreadRoot


class IMessage(IContained, IContainer):

    title = schema.TextLine(
        title=u"Betreff",
        description=u"",
    )

    message = schema.Text(
        title=u"Nachricht",
        description=u"",
    )

    attachment = FileField(
        title=u"Anhang",
        required=False,
        description=u"Bitte waehlen Sie die Datei, die Sie uns senden moechten.",
    )

    filename = schema.TextLine(
        title=u"Dateiname",
        description=u"Der Dateiname der Datei.",
    )

    access_token = schema.TextLine(
        title=u"   ",
        required=False,
    )

    doc_id = schema.TextLine(
        title=u"doc_id",
        required=False,
    )

    sachbearbeiter = schema.TextLine(
        title=u"Sachbearbeiter",
        required=False
    )


class IQuestion(IThreadRoot, IMessage):
    """A question, can be answered
    """
    contains('.IMessage')


class IAnswer(IMessage):
    """An answer, it can't be answered.
    """
