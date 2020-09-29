# -*- coding: utf-8 -*-

from ukh.adhoc.db_setup import z1vrs1aa, z1vrs2aa
from time import localtime, strftime
from sqlalchemy.sql import and_
from z3c.saconfig import Session
from zope.sqlalchemy import mark_changed


def RGStatistik(az, bestaet, unfoid):
    datum = str(strftime("%d.%m.%Y", localtime()))
    upd = z1vrs1aa.update().where(and_(z1vrs1aa.c.az == az)).values(bestaet=bestaet, am=datum, unfoid=unfoid)
    session = Session()
    session.execute(upd)
    mark_changed(session)


def PRStatistik(unfaz, dok_typ, edt_typ):
    datum = str(strftime("%d.%m.%Y", localtime()))
    datum1 = str(strftime("%Y%m%d", localtime()))
    sql = z1vrs2aa.insert(dict(unfaz=unfaz, datum=datum, datum1=datum1, dok_typ=dok_typ, edt_typ=edt_typ))
    session = Session()
    session.execute(sql)
    mark_changed(session)
