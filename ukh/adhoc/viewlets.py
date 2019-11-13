# -*- coding: utf-8 -*-

import grok
import uvcsite

from .auth import get_account
from zope.interface import Interface
from uvc.staticcontent.staticmenuentries import PersonalPanelEntry


class PersonalPanelEntry(PersonalPanelEntry):
    grok.name('ppe')

    @property
    def action(self):
        return self.view.url(get_account(self.request.principal.id), 'personalpanelview')


class StartMenu(uvcsite.MenuItem):
    grok.context(Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)
    grok.title('Startseite')

    @property
    def action(self):
        return self.view.application_url()






class LogoutMenu(uvcsite.MenuItem):
    """ Menu fuer das Logout """
    grok.require('zope.View')
    grok.order(99)
    grok.context(Interface)
    grok.title('Abmelden')
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    @property
    def action(self):
        return self.view.application_url() + '/logout'


class HomeFolderMenuItem(uvcsite.MenuItem):
    """ Menu fuer das Logout """
    grok.require('zope.View')
    grok.order(90)
    grok.context(Interface)
    grok.title('Mein Ordner')
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    @property
    def action(self):
        #print "???????????????????????????????????????????????????????????????"
        #print dir(get_account(self.request.principal.id))
        #print "???????????????????????????????????????????????????????????????"
        return self.view.url(get_account(self.request.principal.id), 'homefolder')


class NachrichtenMenuItem(uvcsite.MenuItem):
    """ Menu fuer das Logout """
    grok.require('zope.View')
    grok.order(95)
    grok.context(Interface)
    grok.title('Nachrichten')
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    @property
    def action(self):
        return self.view.url(get_account(self.request.principal.id), 'nachrichten')
