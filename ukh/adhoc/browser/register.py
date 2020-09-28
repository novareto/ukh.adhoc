# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import re
import uvcsite
import datetime

from ukh.adhoc.resources import css, stepcss
from ukh.adhoc.interfaces import IAccount, IAccountData
from dolmen.forms.base import apply_data_event
from zeam.form.base import makeAdaptiveDataManager
from ukh.adhoc.pdf import Antwort_pdf
from ukh.adhoc.db_setup import z1vrs1aa
from time import localtime, strftime
from sqlalchemy.sql import and_
from z3c.saconfig import Session
from zope.sqlalchemy import mark_changed



grok.templatedir("templates")


def getAlter(gd):
    gdat = "%s.%s.%s" %(str(gd['prsgtt']).zfill(2), str(gd['prsgmm']).zfill(2), str(gd['prsgjj']))
    today = datetime.date.today()
    tag, monat, jahr = gdat.split('.')
    born = datetime.date(int(jahr), int(monat), int(tag))
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


class AccountDataAdapter(grok.Adapter):
    grok.context(IAccount)
    grok.provides(IAccountData)

    def __init__(self, context):
        self.context = context
        self.grunddaten = self.context.getGrundDaten()

    # RegisterF1

    @property
    def active(self):
        return self.context.active

    @active.setter
    def active(self, value):
        self.context.active = value

    # RegisterF2

    @property
    def anrede(self):
        if hasattr(self.context, 'anrede'):
            anrede = self.context.anrede
        else:
            anrede = self.grunddaten.get('ikanr').strip()
        return anrede

    @property
    def nname(self):
        if hasattr(self.context, 'nname'):
            nname = self.context.nname
        else:
            nname = self.grunddaten.get('iknam1').strip()
        return nname

    @property
    def vname(self):
        if hasattr(self.context, 'vname'):
            vname = self.context.vname
        else:
            vname = self.grunddaten.get('iknam2').strip()
        return vname

    @property
    def vsstr(self):
        if hasattr(self.context, 'vsstr'):
            vsstr = self.context.vsstr
        else:
            vsstr = self.grunddaten.get('ikstr').strip()
        return vsstr

    @property
    def vshnr(self):
        if hasattr(self.context, 'vshnr'):
            vshnr = self.context.vshnr
        else:
            vshnr = self.grunddaten.get('ikhnr').strip()
        return vshnr

    @property
    def vsplz(self):
        if hasattr(self.context, 'vsplz'):
            vsplz = self.context.vsplz
        else:
            vsplz = str(self.grunddaten.get('ikhplz'))
        return vsplz

    @property
    def vsort(self):
        if hasattr(self.context, 'vsort'):
            vsort = self.context.vsort
        else:
            vsort = self.grunddaten.get(u'ikhort').strip()
        return vsort

    @property
    def gebdat(self):
        if hasattr(self.context, 'gebdat'):
            gebdat = self.context.gebdat
        else:
            gebdat = "%s.%s.%s" %(str(self.grunddaten.get(u'prsgtt')).zfill(2),
                                  str(self.grunddaten.get(u'prsgmm')).zfill(2),
                                  str(self.grunddaten.get(u'prsgjj')))
        return gebdat

    @property
    def unfdat(self):
        if hasattr(self.context, 'unfdat'):
            unfdat = self.context.unfdat
        else:
            unfdat = "%s.%s.%s" %(str(self.grunddaten.get(u'unfutt')).zfill(2),
                                  str(self.grunddaten.get(u'unfumm')).zfill(2),
                                  str(self.grunddaten.get(u'unfujj')))
        return unfdat

    @property
    def unfzeit(self):
        if hasattr(self.context, 'unfzeit'):
            unfzeit = self.context.unfzeit
        else:
            ret = str(self.grunddaten.get(u'unfstd'))
            lenstd = len(ret)
            if lenstd <= 1:
                unfzeit = '00:00'
            else:
                if lenstd == 3:
                    s = ret[0:1]
                    s = '0' + s
                    m = ret[1:3]
                if lenstd == 4:
                    s = ret[0:2]
                    m = ret[2:4]
                unfzeit = s + ':' + m
        return unfzeit

    @property
    def vsvwl(self):
        return self.context.vsvwl

    @vsvwl.setter
    def vsvwl(self, value):
        self.context.vsvwl = value

    @property
    def vstel(self):
        return self.context.vstel

    @vstel.setter
    def vstel(self, value):
        self.context.vstel = value

    @property
    def handy(self):
        return self.context.handy

    @handy.setter
    def handy(self, value):
        self.context.handy = value

    @property
    def email(self):
        return self.context.email

    @email.setter
    def email(self, value):
        self.context.email = value

    @property
    def email2(self):
        return self.context.email2

    @email2.setter
    def email2(self, value):
        self.context.email2 = value

    # RegisterF3

    @property
    def datenerhebung(self):
        return self.context.datenerhebung

    @datenerhebung.setter
    def datenerhebung(self, value):
        self.context.datenerhebung = value

    # RegisterF4

    @property
    def datenuebermittlung(self):
        return self.context.datenuebermittlung

    @datenuebermittlung.setter
    def datenuebermittlung(self, value):
        self.context.datenuebermittlung = value

    # RegisterF5

    @property
    def jobinfo1(self):
        return self.context.jobinfo1

    @jobinfo1.setter
    def jobinfo1(self, value):
        self.context.jobinfo1 = value

    @property
    def jobinfo2(self):
        return self.context.jobinfo2

    @jobinfo2.setter
    def jobinfo2(self, value):
        self.context.jobinfo2 = value

    @property
    def kkdaten(self):
        return self.context.kkdaten

    @kkdaten.setter
    def kkdaten(self, value):
        self.context.kkdaten = value

    @property
    def hausarzt(self):
        return self.context.hausarzt

    @hausarzt.setter
    def hausarzt(self, value):
        self.context.hausarzt = value

    # ÜBERFLÜSSIG ????????

    @property
    def datenschutz(self):
        return self.context.datenschutz

    @datenschutz.setter
    def datenschutz(self, value):
        self.context.datenschutz = value

    @property
    def telefon(self):
        return self.context.telefon

    @telefon.setter
    def telefon(self, value):
        self.context.telefon = value

    @property
    def ansprechpartner(self):
        return self.context.ansprechpartner

    @ansprechpartner.setter
    def ansprechpartner(self, value):
        self.context.ansprechpartner = value


class RegisterF1(uvcsite.Form):
    grok.context(IAccount)
    label = u"Teilnahme"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    fields = uvcsite.Fields(IAccount).select('active', 'status')
    fields['active'].mode = "radio"
    ignoreContent = False
    dataManager = makeAdaptiveDataManager(IAccountData)

    #@property
    #def unter15jahre(self):
    #    data = self.context.getGrundDaten()
    #    alter = getAlter(data)
    #    a = {}
    #    if alter >= 15:
    #        if self.context.anrede == 'Herr':
    #            a['kombianrede'] = u'Sehr geehrter Herr ' + self.context.ansprechpartner
    #        elif self.context.anrede == 'Frau':
    #            a['kombianrede'] = u'Sehr geehrte Frau ' + self.context.ansprechpartner
    #        else:
    #            a['kombianrede'] = self.context.anrede + ' ' + self.context.ansprechpartner
    #    else:
    #        a['kombianrede'] = u'Sehr geehrte Familie ' + data['iknam1']
    #    return a

    def update(self):
        css.need()

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
        data['status'] = u'bearbeitet'
        apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        if data.get('active') == 'ja':
            self.redirect(self.url(self.context) + '/registerf2')
        else:
            self.redirect(self.url(self.context) + '/registerfinish')


class RegisterF2(RegisterF1):
    label = u"Anmeldung"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    fields = uvcsite.Fields(IAccount).omit(
        'az', 'oid', 'password', 'active', 'status', 'ansprechpartner',
        'anfragedatum', 'telefon', 'datenerhebung', 'datenuebermittlung',
        'kkdaten', 'hausarzt', 'jobinfo1', 'jobinfo2',
        'passworda', 'passwordv', 'gebdat')
    fields['anrede'].mode = "radio"
    ignoreContent = False

    @property
    def unter15jahre(self):
        alter = getAlter(self.context.getGrundDaten())
        a = {}
        if alter >= 15:
            a['kombianrede'] = u'Bitte prüfen Sie zunächst die persönlichen Angaben und ergänzen Sie sie bei Bedarf.'
        else:
            a['kombianrede'] = u'Bitte prüfen Sie zunächst die persönlichen Angaben Ihres Kindes und ergänzen Sie sie bei Bedarf.'
        return a

    def update(self):
        stepcss.need()

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf1')

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        if data['email'] != '':
            checkmail = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$").match
            if not bool(checkmail(data['email'])):
                self.flash(u'Bitte tragen Sie eine gültige E-Mail Adresse ein (E-Mail).')
                return
        if data['email2'] != '':
            checkmail = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$").match
            if not bool(checkmail(data['email2'])):
                self.flash(u'Bitte tragen Sie eine gültige E-Mail Adresse ein (E-Mail Wiederholung).')
                return
        if data['email'] != data['email2']:
            self.flash(u'Die E-Mail Adressen müssen übereinstimmen.')
            return
        apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        self.redirect(self.url(self.context) + '/registerf3')


class RegisterF3(RegisterF1):
    label = u"Datenerhebung"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    fields = uvcsite.Fields(IAccount).select('datenerhebung')
    fields['datenerhebung'].mode = "radio"

    @property
    def unter15jahre(self):
        alter = getAlter(self.context.getGrundDaten())
        a = {}
        a['alter'] = alter
        return a

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf2')

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        self.redirect(self.url(self.context) + '/registerf4')


class RegisterF4(RegisterF1):
    label = u"Datenschutz"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    fields = uvcsite.Fields(IAccount).select('datenuebermittlung')
    fields['datenuebermittlung'].mode = "radio"

    @property
    def unter15jahre(self):
        alter = getAlter(self.context.getGrundDaten())
        a = {}
        a['alter'] = alter
        return a

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf3')

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
        apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        self.redirect(self.url(self.context) + '/registerf5')


class RegisterF5(RegisterF1):
    label = u"Daten"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen."

    @property
    def fields(self):
        fields = uvcsite.Fields(IAccount).select('jobinfo1', 'jobinfo2', 'kkdaten', 'hausarzt')
        alter = getAlter(self.context.getGrundDaten())
        if alter < 15:
            fields['jobinfo1'].title = u'Unfallbetrieb *'
            fields['jobinfo1'].description = u'Bitte nennen Sie uns den Namen und die Anschrift \
                der Kindertagesstätte / des Kindergartens / der Schule.'
            fields['jobinfo2'].title = u'Unfallbringende Tätigkeit *'
            fields['jobinfo2'].description = u'Bitte beschreiben Sie, bei welcher Tätigkeit \
                sich der Unfall ereignete.'
            fields['kkdaten'].title = u'Krankenkasse Ihres Kindes *'
            fields['hausarzt'].title = u'Kinder-/Hausärztin oder Kinder-/Hausarzt *'
            fields['hausarzt'].description = u'Bitte nennen Sie uns den Namen und die Anschrift \
                der Kinder-/Hausärztin oder des Kinder-/Hausarztes.'
        return fields

    @property
    def unter15jahre(self):
        alter = getAlter(self.context.getGrundDaten())
        a = {}
        if alter >= 15:
            a['kombianrede'] = u'Im letzten Schritt bitten wir Sie noch um einige Informationen, die uns helfen, Ihren Fall zügig zu bearbeiten.'
        else:
            a['kombianrede'] = u'Im letzten Schritt bitten wir Sie noch um einige Informationen, die uns helfen, den Fall Ihres Kindes zügig zu bearbeiten.'
        return a

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf4')

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        context = self.context
        grunddaten = self.context.getGrundDaten()
        Antwort_pdf(context, grunddaten, u'zusage')
        datum = str(strftime("%d.%m.%Y", localtime()))
        upd = z1vrs1aa.update().where(and_(z1vrs1aa.c.az == context.az)).values(bestaet='J', am=datum, unfoid=str(grunddaten['unfoid']))
        session = Session()
        session.execute(upd)
        mark_changed(session)
        self.redirect(self.application_url())


class RegisterFinish(uvcsite.Form):
    grok.context(IAccount)
    label = u"Teilnahme"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    ignoreContent = False
    dataManager = makeAdaptiveDataManager(IAccountData)

    def update(self):
        context = self.context
        grunddaten = self.context.getGrundDaten()
        Antwort_pdf(context, grunddaten, u'absage')
        datum = str(strftime("%d.%m.%Y", localtime()))
        upd = z1vrs1aa.update().where(and_(z1vrs1aa.c.az == context.az)).values(bestaet='N', am=datum, unfoid=str(grunddaten['unfoid']))
        session = Session()
        session.execute(upd)
        mark_changed(session)
        css.need()
