# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite

from .resources import css, stepcss
#from .resources import step1js
from .auth import get_account
from .interfaces import IAccount, IAccountData
from ukh.adhoc.interfaces import IUKHAdHocApp
from uvc.tbskin.resources import TBSkinViewlet
from zope.interface import Interface
from bgetem.lv1101.content import AddForm
from dolmen.forms.base import Fields, set_fields_data, apply_data_event
from uvc.adhoc import content
from dolmen.content import schema
from zope.dottedname.resolve import resolve
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from uvc.adhoc.interfaces import IAdHocContent
from zeam.form.base import makeAdaptiveDataManager

from uvc.adhoc import BaseAddView

from .pdf import Absage_pdf, Zusage_pdf

grok.templatedir("templates")

import sys
reload(sys)
sys.setdefaultencoding('utf8')


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
        if 'anrede' in dir(self.context):
            anrede = self.context.anrede
        else:
            anrede = self.grunddaten.get('ikanr').strip()
        return anrede
        #return self.grunddaten.get('ikanr').strip()

    @property
    def nname(self):
        if 'nname' in dir(self.context):
            nname = self.context.nname
        else:
            nname = self.grunddaten.get('iknam1').strip()
        return nname
        #return self.grunddaten.get('iknam1').strip()

    @property
    def vname(self):
        if 'vname' in dir(self.context):
            vname = self.context.vname
        else:
            vname = self.grunddaten.get('iknam2').strip()
        return vname
        #return self.grunddaten.get('iknam2').strip()

    @property
    def vsstr(self):
        if 'vsstr' in dir(self.context):
            vsstr = self.context.vsstr
        else:
            vsstr = self.grunddaten.get('ikstr').strip()
        return vsstr
        #return self.grunddaten.get('ikstr').strip()

    @property
    def vshnr(self):
        if 'vshnr' in dir(self.context):
            vshnr = self.context.vshnr
        else:
            vshnr = self.grunddaten.get('ikhnr').strip()
        return vshnr
        #return self.grunddaten.get('ikhnr').strip()

    @property
    def vsplz(self):
        if 'vsplz' in dir(self.context):
            vsplz = self.context.vsplz
        else:
            vsplz = str(self.grunddaten.get('ikhplz'))
        return vsplz
        #return str(self.grunddaten.get('ikhplz'))

    @property
    def vsort(self):
        if 'vsort' in dir(self.context):
            vsort = self.context.vsort
        else:
            vsort = str(self.grunddaten.get(u'ikhort').strip())
        return vsort
        #return self.grunddaten.get('ikhort').strip()

    @property
    def gebdat(self):
        if 'gebdat' in dir(self.context):
            gebdat = self.context.gebdat
        else:
            ret = self.grunddaten
            t = str(ret['prsgtt'])
            m = str(ret['prsgmm'])
            j = str(ret['prsgjj'])
            if len(t) == 1:
                t = '0' + t
            if len(m) == 1:
                m = '0' + m
            gebdat = t + '.' + m + '.' + j
        return gebdat

    @property
    def unfdat(self):
        if 'unfdat' in dir(self.context):
            unfdat = self.context.unfdat
        else:
            ret = self.grunddaten
            t = str(ret['unfutt'])
            m = str(ret['unfumm'])
            j = str(ret['unfujj'])
            if len(t) == 1:
                t = '0' + t
            if len(m) == 1:
                m = '0' + m
            unfdat = t + '.' + m + '.' + j
        return unfdat

    @property
    def unfzeit(self):
        if 'unfzeit' in dir(self.context):
            unfzeit = self.context.unfzeit
        else:
            ret = self.grunddaten
            lenstd = len(str(ret['unfstd']))
            if lenstd == 3:
                s = str(ret['unfstd'])[0:1]
                s = '0' + s
                m = str(ret['unfstd'])[1:3]
            if lenstd == 4:
                s = str(ret['unfstd'])[0:2]
                m = str(ret['unfstd'])[2:4]
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
    def kkdaten(self):
        return self.context.kkdaten

    @kkdaten.setter
    def kkdaten(self, value):
        self.context.kkdaten = value

    @property
    def kkvsnummer(self):
        return self.context.kkvsnummer

    @kkvsnummer.setter
    def kkvsnummer(self, value):
        self.context.kkvsnummer = value

    @property
    def hausarzt(self):
        return self.context.hausarzt

    @hausarzt.setter
    def hausarzt(self, value):
        self.context.hausarzt = value

    @property
    def zusatzarzt(self):
        return self.context.zusatzarzt

    @zusatzarzt.setter
    def zusatzarzt(self, value):
        self.context.zusatzarzt = value

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
        self.context.telefon= value

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

    def update(self):
        css.need()

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
        data['status'] = u'bearbeitet'
        changes = apply_data_event(self.fields, self.context, data)
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
        'kkdaten', 'kkvsnummer', 'hausarzt', 'zusatzarzt')
    fields['anrede'].mode = "radio"
    ignoreContent = False

    def update(self):
        stepcss.need()

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf1')

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        self.redirect(self.url(self.context) + '/registerf3')


class RegisterF3(RegisterF1):
    label = u"Datenerhebung"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    fields = uvcsite.Fields(IAccount).select('datenerhebung')
    fields['datenerhebung'].mode = "radio"

    def update(self):
        print "################################################################"

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf2')

    @uvcsite.action('Speichern & Weiter')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        self.redirect(self.url(self.context) + '/registerf4')


class RegisterF4(RegisterF1):
    label = u"Datenschutz"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"
    fields = uvcsite.Fields(IAccount).select('datenuebermittlung')
    fields['datenuebermittlung'].mode = "radio"

    def update(self):
        print "REGISTERF4   ###################################################"

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf3')

    @uvcsite.action('Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
        changes = apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        self.redirect(self.url(self.context) + '/registerf5')


class RegisterF5(RegisterF1):
    label = u"Daten"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"

    fields = uvcsite.Fields(IAccount).select('kkdaten', 'kkvsnummer', 'hausarzt', 'zusatzarzt')

    def update(self):
        print "REGISTERF5   ###################################################"

    @uvcsite.action(u'Zurück')
    def handle_back(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.redirect(self.url(self.context) + '/registerf4')

    @uvcsite.action('Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")
            return
        changes = apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        context = self.context
        grunddaten = self.context.getGrundDaten()
        Zusage_pdf(context, grunddaten)
        #self.redirect(self.url(self.context) + '/registerf6')
        self.redirect(self.application_url())


#class RegisterFinish(uvcsite.Page):
#    grok.context(IAccount)
#    grok.name('registerfinish')
#
#    def render(self):
#        return u"HALLO WELT"

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
        Absage_pdf(context, grunddaten)
        css.need()

