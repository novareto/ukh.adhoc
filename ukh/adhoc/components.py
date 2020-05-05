# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2013 NovaReto GmbH
# # cklinger@novareto.de

import os
import grok
import locale
import uvcsite

from persistent import Persistent
from persistent.list import PersistentList
from zope.interface import implementer
from ukh.adhoc.interfaces import IAccount, IDocumentInfo
from z3c.saconfig import Session
from sqlalchemy.sql import select
from sqlalchemy.sql import and_
from .db_setup import c1unf1aa, c1prs1aa, avika1aa
from .db_setup import zczve1aa, zckto1aa
from uvc.letterbasket.components import LetterBasket
from dolmen.security.policies.principalrole import ExtraRoleMap
from zope.securitypolicy.securitymap import SecurityMap
from zope.securitypolicy.interfaces import Allow
from zope.container.interfaces import INameChooser

# Tausendertrennzeichen
locale.setlocale(locale.LC_ALL, "")

def c_locale(zahl):
    return locale.currency(zahl, False, True)


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

    def getGrundDaten(self):
        if os.environ['ADHOC_TEST'] == "True":
            from ukh.adhoc.lib.testdata import gd
            return gd
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
        nd= {}
        for k, v in datensatz.items():
            nd[k] = str(v)
        print
        print nd
        print
        return datensatz

    def getVersichertenkonto(self):
        sql = select(
            [c1unf1aa, zczve1aa, zckto1aa],
            and_(
                zckto1aa.c.ktozve == zczve1aa.c.zveoid,
                zczve1aa.c.zveobj == c1unf1aa.c.unfoid,
                c1unf1aa.c.unfaz == self.az))
        session = Session()
        daten = session.execute(sql).fetchall()
        vkonto = []
        ambheil = 0
        staheil = 0
        hilfsmi = 0
        entgelt = 0
        reiseko = 0
        renten = 0
        pflege = 0
        hhhilfe = 0
        mehrlei = 0
        sachsch = 0
        sozteil = 0
        leiteil = 0
        for x in daten:
            kto = str(x['ktokto']) + str(x['ktoktu'])
            if kto in ['4000', '4001', '4002', '4003', '4007', '4500', '4830', '4820']:
                ambheil += x['ktosol']
                ambheil -= x['ktohab']
            if kto in ['4600', '4601', '4607']:
                staheil += x['ktosol']
                staheil -= x['ktohab']
            if kto in ['4004', '4005']:
                hilfsmi += x['ktosol']
                hilfsmi -= x['ktohab']
            if kto in ['4700', '4701', '4750', '4840', '4910', '4920', '4940', '4883', '4890']:
                entgelt += x['ktosol']
                entgelt -= x['ktohab']
            if kto in ['4850', '4950', '4951']:
                reiseko += x['ktosol']
                reiseko -= x['ktohab']
            if kto in ['5000', '5010', '5020', '5030', '5040', '5050', '5100', '5110', '5120', '5200', '5210', '5250']:
                renten += x['ktosol']
                renten -= x['ktohab']
            if kto in ['4650', '4800', '4801', '4810']:
                pflege += x['ktosol']
                pflege -= x['ktohab']
            if kto in ['4860', '4960', '4884']:
                hhhilfe += x['ktosol']
                hhhilfe -= x['ktohab']
            if kto in ['5600', '5610', '5620']:
                mehrlei += x['ktosol']
                mehrlei -= x['ktohab']
            if kto in ['5650']:
                sachsch += x['ktosol']
                sachsch -= x['ktohab']
            if kto in ['4880', '4881', '4882', '4885', '4886', '4887']:
                sozteil += x['ktosol']
                sozteil -= x['ktohab']
            if kto in ['4900', '4901', '4902', '4903', '4904', '4980', '4981', '4982']:
                leiteil += x['ktosol']
                leiteil -= x['ktohab']
        summe = 0
        for z in [['Ambulante Heilbehandlung', ambheil],
                  [u'Stationäre Heilbehandlung', staheil],
                  [u'Hilfsmittel', hilfsmi],
                  [u'Entgeltersatzleistungen', entgelt],
                  [u'Reisekosten', reiseko],
                  [u'Renten', renten],
                  [u'Pflege', pflege],
                  [u'Haushaltshilfe', hhhilfe],
                  [u'Mehrleiszungen', mehrlei],
                  [u'Sachschäden', sachsch],
                  [u'Soziale Teilhabe', sozteil],
                  [u'Leistungen zur Teilhabe', leiteil],
                  ]:
            if z[1] > 0:
                summe += z[1]
                z[1] = str(c_locale(z[1]))
                vkonto.append(z)
        vkonto.append([u'Gesamtbetrag in EUR', str(c_locale(summe))])
        return vkonto


    def checkPassword(self, password, gebdate):
        if password != self.password:
            return False
        gd = self.getGrundDaten()
        gdatum = "%s.%s.%s" %(str(gd['prsgtt']).zfill(2), str(gd['prsgmm']).zfill(2), str(gd['prsgjj']))
        print gdatum
        if gebdate != gdatum:
            return False
        return True

    def add(self, content):
        name = INameChooser(self).chooseName(content.__name__ or '', content)
        self[name] = content


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
