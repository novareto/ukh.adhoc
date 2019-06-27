# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite


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

from uvc.adhoc.interfaces import IAdHocContent


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


class LandingPage(uvcsite.Page):
    grok.name("index")
    grok.context(IAccount)

    def update(self):
        if not self.context.active:
            self.redirect(self.url(self.context, 'register'))


class Register(uvcsite.Form):
    grok.context(IAccount)
    label = u"Anmeldung"
    description = u"Bitte vervollständigen Sie folgende Angaben um den \
        'Versicherten Service' der UKH zu nutzen"

    fields = uvcsite.Fields(IAccount).omit('az', 'oid', 'password')
    ignoreContent = False

    @uvcsite.action('Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u"Bitte überprüfen Sie Ihre eingaben")

        changes = apply_data_event(self.fields, self.context, data)
        self.flash(u'Speichern erfolgreich.')
        return self.redirect(self.application_url())



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
