# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite

from persistent import Persistent
from persistent.list import PersistentList
from zope.interface import implementer
from ukh.adhoc.interfaces import IAccount, IDocumentInfo
from z3c.saconfig import Session
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from .db_setup import c1unf1aa, c1prs1aa, avika1aa
from uvc.letterbasket.components import LetterBasket
from dolmen.security.policies.principalrole import ExtraRoleMap
from zope.securitypolicy.securitymap import SecurityMap
from zope.securitypolicy.interfaces import Allow


class MasterUserRoleManager(ExtraRoleMap, grok.Adapter):
    grok.context(IAccount)

    def _compute_extra_data(self):
        extra_map = SecurityMap()
        if uvcsite.getPrincipal().id == self.context.az:
            extra_map.addCell('uvc.Editor', self.context.az, Allow)
        return extra_map



@implementer(IAccount)
class Account(grok.Container):

    def __init__(self, az, password, email, oid, ansprechpartner, anrede,
                 datenerhebung, datenuebermittlung, telefon, active, status,
                 anfragedatum, sb_name, sb_mail):
        super(Account, self).__init__()
        self.az = az
        self.password = password
        self.email = email
        self.oid = oid
        self.id = az
        self.ansprechpartner = ansprechpartner
        self.anrede = anrede
        self.datenerhebung = datenerhebung
        self.datenuebermittlung = datenuebermittlung
        self.telefon = telefon
        self.active = active
        self.status = status
        self.anfragedatum = anfragedatum
        self.sb_name = sb_name
        self.sb_mail = sb_mail
        self['nachrichten'] = LetterBasket()

    def values(self):
        return [x for x in super(Account, self).values() if x.__name__ != 'nachrichten']

    def getGrundDaten(self):
        d1 = select(
            [c1unf1aa, c1prs1aa],
            and_(c1prs1aa.c.prsoid == c1unf1aa.c.unfprs,
                c1unf1aa.c.unfaz == self.az))
        session = Session()
        daten1 = session.execute(d1).fetchall()
        d2 = select(
            [avika1aa],
            and_(avika1aa.c.ikkl == str(daten1[0]['prsikn'])[0:3],
            avika1aa.c.ikbs == str(daten1[0]['prsikn'])[3:10]))
        prsdaten = session.execute(d2).fetchall()
        datensatz = {}
        datensatz.update(dict(prsdaten[0]))
        datensatz.update(dict(daten1[0]))
        if datensatz['ikanr'] == 1:
            datensatz['ikanr'] = u'Frau'
        else:
            datensatz['ikanr'] = u'Herr'
        return datensatz

    def checkPassword(self, password):
        if password != self.password:
            return False
        return True


from uvc.adhoc.components import AdHocContent
from hurry.workflow.interfaces import IWorkflowState

class UKHAdHocContent(AdHocContent):

    @property
    def doc_title(self):
        return grok.title.bind().get(self)

    @property
    def doc_name(self):
        return grok.name.bind().get(self)

    @property
    def state(self):
        from uvcsite.workflow.basic_workflow import titleForState
        return titleForState(IWorkflowState(self).getState())



@implementer(IDocumentInfo)
class Document(Persistent):
    doc_type = None
    defaults = None

    def __init__(self, doc_type, defaults):
        super(Document, self).__init__()
        self.doc_type = doc_type
        self.defaults = defaults
