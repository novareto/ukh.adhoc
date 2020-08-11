#!/usr/bin/env python                                                                                                                             
# -*- coding: utf-8 -*-

import os
import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue
from time import localtime, strftime
from ..pdf import cutrow, pdf_seitenkopf_master, ueberschrift, antwort


bcp = '/'.join(__file__.split('/')[:-2])


def Nachricht_pdf(dat, nname, vname, tmp):
    ft = 90
    bt = 90
    datum = str(strftime("%d.%m.%Y", localtime()))
    uhrzeit = str(strftime("%H:%M", localtime()))
    if tmp is None:
        datum2 = str(strftime("%Y_%m_%d_%H_%M_%S", localtime()))
        verzeichnis = '/ausgang/fax133a'
        dateiname = datum2 + '_' + dat.principal.id + '_Nachricht.pdf'
        saveverzeichnis = verzeichnis + '/' + dateiname
    else:
        saveverzeichnis = tmp
    # Layout
    c = canvas.Canvas(saveverzeichnis, pagesize=A4)
    c.setAuthor("UKH")
    c.setTitle(u'Druckversion')
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    # Seite 1 - Deckblatt
    seite = 1
    c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
    y1 = 25.0
    x1 = 2.2
    x2 = 8.2
    c.setFillColor(black)
    c.setFont(schriftart, 11)
    c.drawString(x1 * cm, y1 * cm, u"Aktenzeichen:")
    c.drawString(x2 * cm, y1 * cm, dat.principal.id)
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Name:")
    c.drawString(x2 * cm, y1 * cm, nname)
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Vorname:")
    c.drawString(x2 * cm, y1 * cm, vname)
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Formular Typ:")
    c.drawString(x2 * cm, y1 * cm, u"Nachricht")
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Formular Bezeichnung:")
    c.drawString(x2 * cm, y1 * cm, u"Nachricht")
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"EDT DocTyp:")
    c.drawString(x2 * cm, y1 * cm, u"004.001")
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Eingangsdatum:")
    c.drawString(x2 * cm, y1 * cm, datum)
    # ----------------------------------------------
    # Seitenwechsel
    # ----------------------------------------------
    c.showPage()
    seite += 1
    c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
    y1 = 26.5
    # ----------------------------------------------
    # Fragen / Antworten
    # ###############################################################################
    # # 1                                                                           # 
    # ###############################################################################
    text = cutrow(dat.message, 100)
    # Platzbedarf ermitteln
    lt = len(text) * 0.4
    lt += 4
    # ----------------------------------------------
    # Gegebenenfalls Seitenwechsel einleiten
    # ----------------------------------------------
    if lt > y1:
        c.showPage()
        seite += 1
        c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
        y1 = 26.5
    # ----------------------------------------------
    ftext = cutrow(u'Betreff', ft)
    y1 = ueberschrift(c, schriftartfett, ftext, x1, y1, 11)
    btext = cutrow(dat.title, bt)
    y1 = ueberschrift(c, schriftartfett, btext, x1, y1, 9)
    y1 -= 1.0
    ftext = cutrow(u'Nachricht', ft)
    y1 = ueberschrift(c, schriftartfett, ftext, x1, y1, 11)
    y1 = antwort(c, schriftart, text, x1, y1)
    # ----------------------------------------------
    # Seitenumbruch
    c.showPage()
    # ENDE und Save
    c.save()
