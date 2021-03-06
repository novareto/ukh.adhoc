# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite

from dolmen.content import schema
from dolmen.forms.base import Fields, set_fields_data, apply_data_event

from ukh.adhoc.auth import get_account
from ukh.adhoc.interfaces import IAccount, IUKHAdHocApp
from ukh.adhoc.resources import badge_css, ah_css, css, meinedatencss, kontocss
from ukh.fahrtkosten.views import IFahrtkosten
from ukhtheme.grok.layout import ILayer

from uvc.adhoc import content
from uvc.adhoc.views import BaseAddView
from uvc.adhoc.interfaces import IAdHocContent
from uvc.layout.forms.components import AddForm
from uvc.staticcontent.staticmenuentries import PersonalPanel
from uvc.tbskin.resources import TBSkinViewlet
from uvc.tbskin.views import FieldMacros

import uvcsite.plugins
from uvcsite.extranetmembership.enms import ChangePassword
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.dottedname.resolve import resolve
from zope.interface import Interface
from zope.traversing.interfaces import IBeforeTraverseEvent
from ukh.adhoc.interfaces import IUKHAdHocLayer
from grokcore.chameleon.components import ChameleonPageTemplateFile

from ukh.adhoc.browser.register import getAlter
from hurry.workflow.interfaces import IWorkflowState
from hurry.workflow.interfaces import IWorkflowInfo

grok.templatedir("templates")


class FieldMacros(FieldMacros):
    grok.layer(IUKHAdHocLayer)
    template = ChameleonPageTemplateFile('templates/fieldtemplates.cpt')



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
        if name == 'plugins':
            return uvcsite.plugins.PluginsPanel('plugins', self.context)
        return get_account(name)


@grok.subscribe(IBeforeTraverseEvent)
def redirect_on_empty_props(event):
    principal = event.request.principal
    if IUnauthenticatedPrincipal.providedBy(principal):
        return
    if "stammdaten" in event.request.environment.get("PATH_INFO"):
        return
    if event.request.principal.id == u"servicetelefon-0":
        return


class LandingPage(uvcsite.Page):
    grok.name("index")
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        if self.context.status == "bearbeitet":
            if 'kkdaten' not in dir(self.context):
                self.redirect(self.url(self.context, "registerf1"))
            if self.context.active == "nein":
                self.redirect(self.url(self.context, "registerfinish"))
        self.context.statustext = u"Momentan haben wir keine Geschäftsfälle für Sie"
        zf = 0
        for item in self.values():
            if item.state == "Entwurf":
                zf += 1
                self.context.statustext = (
                    u"Momentan haben wir folgende Geschäftsfälle für Sie"
                )
        self.context.anzahl = zf
        zn = 0
        #for item in self.context.values():
        #    if item.title == 'Postfach':
        #        postfach = item
        #for nachricht in postfach.values():
        #    user = str(nachricht.principal)
        #    if 'zope.anybody' in user:
        #        status = str(IWorkflowState(nachricht).getState())
        #        test = dir(IWorkflowInfo(nachricht).context)
        #        if 'sent' in status:
        #            zn += 1
        from ukh.adhoc.letterbasket.views import IMessageTableItem
        for message in self.context['nachrichten'].values():
            ma = IMessageTableItem(message)
            if ma.css_class() == 'glyphicon glyphicon-envelope':
                zn += 1
        self.context.anzahlungelesen = zn
        badge_css.need()

    def values(self):
        from ukh.fahrtkosten.views import IFahrtkosten
        return [
            x
            for x in self.context.values()
            if (x.__name__ != "nachrichten" and not IFahrtkosten.providedBy(x))
        ]


class Formulare(uvcsite.Page):
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        if self.context.status == "bearbeitet":
            if self.context.active == "nein":
                self.redirect(self.url(self.context, "registerfinish"))
        self.context.statustext = u"Momentan haben Sie keine offenen Formulare"
        for item in self.values():
            if item.state == "Entwurf":
                self.context.statustext = (
                    u"Momentan haben Sie folgende offene Formulare zu bearbeiten:"
                )

    def values(self):
        #return [x for x in self.context.values() if (x.__name__ != "nachrichten")]
        return [x for x in self.context.values() if (x.__name__ != "nachrichten") if (x.state == "Entwurf")]


class Homefolder(uvcsite.Page):
    grok.name("homefolder")
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        if self.context.status == "bearbeitet":
            if 'kkdaten' not in dir(self.context):
                self.redirect(self.url(self.context, "registerf1"))
            if self.context.active == "nein":
                self.redirect(self.url(self.context, "registerfinish"))

    def values(self):
        from ukh.fahrtkosten.views import IFahrtkosten
        return [x for x in self.context.values() if x.__name__ != "nachrichten"]


class PersonalPanel(PersonalPanel):
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        if self.context.status == "bearbeitet":
            if 'kkdaten' not in dir(self.context):
                self.redirect(self.url(self.context, "registerf1"))
            if self.context.active == "nein":
                self.redirect(self.url(self.context, "registerfinish"))


class ChangePassword(ChangePassword):
    grok.context(IAccount)
    fields = uvcsite.Fields(IAccount).select("passworda", "password", "passwordv")

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        if self.context.status == "bearbeitet":
            if self.context.active == "nein":
                self.redirect(self.url(self.context, "registerfinish"))

    @uvcsite.action("Speichern")
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash("Es sind Fehler aufgetreten", type="error")
            return
        if data["passworda"] != self.context.password:
            self.flash(u"Das alte Passwort ist nicht korrekt!")
            return
        if data["password"] != data["passwordv"]:
            self.flash(
                u'Die Einträge unter "neues Passwort" und "Bestätigung" müssen identisch sein!'
            )
            return
        self.context.password = data["password"]
        self.flash(u"Ihr Passwort wurde erfolgreich geändert.")
        self.redirect(self.url(self.context))


class MeinKonto(uvcsite.Form):
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        kontocss.need()

    @property
    def daten(self):
        dat = self.context.getVersichertenkonto()
        return dat


class MeineFahrtkosten(uvcsite.Form):
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))


class Kontakt(uvcsite.Form):
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))


class MeineDaten(uvcsite.Form):
    grok.context(IAccount)

    def update(self):
        if self.context.status != "bearbeitet":
            self.redirect(self.url(self.context, "registerf1"))
        if self.context.status == "bearbeitet":
            if 'kkdaten' not in dir(self.context):
                self.redirect(self.url(self.context, "registerf1"))
            if self.context.active == "nein":
                self.redirect(self.url(self.context, "registerfinish"))
        meinedatencss.need()

    @property
    def unter15jahre(self):
        alter = getAlter(self.context.getGrundDaten())
        a = {}
        if alter >= 15:
            a['ueberschrift'] = u'Wir haben folgende Daten von Ihnen:'
        else:
            a['ueberschrift'] = u'Wir haben folgende Daten Ihres Kindes:'
        a['alter'] = alter
        return a

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


from uvcsite.content.views import Add


class FormDisplay(uvcsite.Form):
    grok.context(IAdHocContent)
    grok.baseclass()
    grok.name('fd')

    @property
    def fields(self):
        return uvcsite.Fields(*self.context.schema) #.omit( "title", "docid", "doc_type", "anschreiben")

    def update(self):
        ah_css.need()


class Form(uvcsite.Form):
    grok.context(IAdHocContent)
    grok.name("edit")
    grok.require("zope.View")

    ignoreContext = False
    ignoreContent = False

    @property
    def label(self):
        return self.context.doc_title

    description = u"Bitte geben Sie uns folgende Informationen"

    @property
    def fields(self):
        return uvcsite.Fields(*self.context.schema).omit(
            "title", "docid", "doc_type", "anschreiben"
        )

    @uvcsite.action(u"Weiter")
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            return
        changes = apply_data_event(self.fields, self.context, data)
        if changes:
            from uvc.layout.forms.event import AfterSaveEvent
            #grok.notify(AfterSaveEvent(self.context, self.request))
        else:
            self.flash("Kein Änderung", type="info")
        self.flash(u"Speichern erfolgreich.")
        return self.redirect(self.url(self.context))

    #@uvcsite.action(u"Abbrechen")
    #def handle_cancel(self):
    #    self.flash(u"Der Vorgang wurde abgebrochen.")
    #    return self.redirect(self.application_url())


class Logout(grok.View):
    """
    Menueeintrag zum Ausloggen
    mit Cookie loeschen.
    """

    grok.context(Interface)
    grok.title(u"Abmelden")

    KEYS = ("beaker.session.id", "dolmen.authcookie", "auth_pubtkt")

    def update(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            for key in self.KEYS:
                self.request.response.expireCookie(key, path="/", domain="ukh.de")

    def render(self):
        self.request.response.expireCookie("beaker.session.id", path="/")
        self.request.response.expireCookie("dolmen.authcookie", path="/")
        self.request["beaker.session"].delete()
        url = self.application_url() + "/index"
        self.response.redirect(url)
