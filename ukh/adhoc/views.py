# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite

from .resources import css, meinedatencss, kontocss
#from .resources import step1js
from .auth import get_account
from .interfaces import IAccount
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
from uvc.staticcontent.staticmenuentries import PersonalPanel
from uvcsite.extranetmembership.enms import ChangePassword
from ukh.fahrtkosten.views import IFahrtkosten
from uvc.adhoc import BaseAddView


grok.templatedir("templates")


class Index(uvcsite.Page):
    grok.context(IUKHAdHocApp)

    def render(self):
        self.request.response.redirect(
            "%s/%s" % (self.application_url(), self.request.principal.id)
        )
        return


class PrincipalTraverser(grok.Traverser):
    grok.context(IUKHAdHocApp)

    def traverse(self, name):
        return get_account(name)


from zope.traversing.interfaces import IBeforeTraverseEvent
from zope.authentication.interfaces import IUnauthenticatedPrincipal
@grok.subscribe(IBeforeTraverseEvent)
def redirect_on_empty_props(event):
    principal = event.request.principal
    if IUnauthenticatedPrincipal.providedBy(principal):
        return
    if 'stammdaten' in event.request.environment.get('PATH_INFO'):
        return
    if event.request.principal.id == u'servicetelefon-0':
        return


class LandingPage(uvcsite.Page):
    grok.name("index")
    grok.context(IAccount)

    def update(self):
        z = 0
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        if self.context.status == 'bearbeitet':
            if self.context.active == 'nein':
                self.redirect(self.url(self.context, 'registerfinish'))
        self.context.statustext = u'Momentan haben wir keine Geschäftsfälle für Sie'
        for item in self.values():
            if item.state == 'Entwurf':
                z += 1
                self.context.statustext = u'Momentan haben wir folgende Geschäftsfälle für Sie'
        self.context.anzahl = z

    def values(self):
        from ukh.fahrtkosten.views import IFahrtkosten
        return [x for x in self.context.values() if (x.__name__ != 'nachrichten' and not IFahrtkosten.providedBy(x))]


class Formulare(uvcsite.Page):
    grok.context(IAccount)

    def update(self):
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        if self.context.status == 'bearbeitet':
            if self.context.active == 'nein':
                self.redirect(self.url(self.context, 'registerfinish'))
        self.context.statustext = u'Momentan haben Sie keine offenen Formulare'
        for item in self.values():
            if item.state == 'Entwurf':
                self.context.statustext = u'Momentan haben Sie folgende offene Formulare zu bearbeiten:'

    def values(self):
        return [x for x in self.context.values() if (x.__name__ != 'nachrichten' )]


class Homefolder(uvcsite.Page):
    grok.name('homefolder')
    grok.context(IAccount)

    def update(self):
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        if self.context.status == 'bearbeitet':
            if self.context.active == 'nein':
                self.redirect(self.url(self.context, 'registerfinish'))

    def values(self):
        from ukh.fahrtkosten.views import IFahrtkosten
        return [x for x in self.context.values() if x.__name__ != 'nachrichten']


class PersonalPanel(PersonalPanel):
    grok.context(IAccount)

    def update(self):
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        if self.context.status == 'bearbeitet':
            if self.context.active == 'nein':
                self.redirect(self.url(self.context, 'registerfinish'))


class ChangePassword(ChangePassword):
    grok.context(IAccount)
    fields = uvcsite.Fields(IAccount).select('passworda', 'password', 'passwordv')

    def update(self):
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        if self.context.status == 'bearbeitet':
            if self.context.active == 'nein':
                self.redirect(self.url(self.context, 'registerfinish'))

    @uvcsite.action('Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        if data['passworda'] != self.context.password:
            self.flash(u'Das alte Passwort ist nicht korrekt!')
            return
        if data['password'] != data['passwordv']:
            self.flash(u'Die Einträge unter "neues Passwort" und "Bestätigung" müssen identisch sein!')
            return
        self.context.password = data['password']
        self.flash(u'Ihr Passwort wurde erfolgreich geändert.')
        self.redirect(self.url(self.context))


class MeinKonto(uvcsite.Form):
    grok.context(IAccount)

    def update(self):
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        kontocss.need()

    @property
    def daten(self):
        dat = self.context.getVersichertenkonto()
        return dat


class MeineDaten(uvcsite.Form):
    grok.context(IAccount)

    def update(self):
        if self.context.status != 'bearbeitet':
            self.redirect(self.url(self.context, 'registerf1'))
        if self.context.status == 'bearbeitet':
            if self.context.active == 'nein':
                self.redirect(self.url(self.context, 'registerfinish'))
        meinedatencss.need()

    @property
    def daten(self):
        return self.context


class TBSkinViewlet(TBSkinViewlet):
    pass


class UKHBaseAddView(BaseAddView):
    grok.baseclass()
    grok.context(Interface)

    def create(self, data):
        content = super(UKHBaseAddView, self).create(data)
        return content


class AddForm(AddForm):
    grok.context(Interface)


class EditForm(uvcsite.Form):
    grok.context(IAdHocContent)
    grok.name('edit')
    grok.require('zope.View')

    ignoreContext = False
    ignoreContent = False

    @property
    def label(self):
        return self.context.doc_title

    description = u"Bitte geben Sie uns folgende Informationen"

    @property
    def fields(self):
        return uvcsite.Fields(*self.context.schema).omit('title', 'docid', 'doc_type', 'anschreiben')


    @uvcsite.action(u"Speichern")
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            return
        changes = apply_data_event(self.fields, self.context, data)
        if changes:
            from uvc.layout.forms.event import AfterSaveEvent
            grok.notify(AfterSaveEvent(self.context, self.request))
        else:
            self.flash('Kein Änderung', type="info")
        self.flash(u'Speichern erfolgreich.')
        return self.redirect(self.application_url())

    @uvcsite.action(u"Abbrechen")
    def handle_cancel(self):
        self.flash(u'Der Vorgang wurde abgebrochen.')
        return self.redirect(self.application_url())


class Logout(grok.View):
    """
    Menueeintrag zum Ausloggen
    mit Cookie loeschen.
    """
    grok.context(Interface)
    grok.title(u'Abmelden')

    KEYS = ("beaker.session.id", "dolmen.authcookie", "auth_pubtkt")

    def update(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            for key in self.KEYS:
                self.request.response.expireCookie(key, path='/', domain="ukh.de")

    def render(self):
        self.request.response.expireCookie('beaker.session.id', path='/')
        self.request.response.expireCookie('dolmen.authcookie', path='/')
        self.request['beaker.session'].delete()
        url = self.application_url()+'/index'
        self.response.redirect(url)
