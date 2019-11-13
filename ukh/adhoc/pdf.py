#!/usr/bin/env python                                                                                                                             
# -*- coding: utf-8 -*-

import os
import datetime


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue
from time import localtime, strftime

def getDaleDir():
    """
    Gibt das Directory für die Speicherung der Dokumente
    zurück und legt das Verzeichnis an, wenn es nicht
    bereits existiert.
    """
    basepath = '/ausgang/fax133'
    archdir = datetime.datetime.now().strftime('%y/%m/%d')
    path = '%s/%s' % (basepath, archdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def Absage_pdf(data, grunddaten):
    # Dateiname
    datum = str(strftime("%d.%m.%Y", localtime()))
    datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
    verzeichnis = getDaleDir()
    dateiname = datum2 + '_' + data.az + '.pdf'
    saveverzeichnis = verzeichnis + '/' + dateiname
    # Grunddaten
    j = str(grunddaten['unfujj'])
    m = str(grunddaten['unfumm'])
    t = str(grunddaten['unfutt'])
    if len(m) == 1:
        m = '0' + m
    if len(t) == 1:
        t = '0' + t
    unfdat = t + '.' + m + '.' + j
    j = str(grunddaten['prsgjj'])
    m = str(grunddaten['prsgmm'])
    t = str(grunddaten['prsgtt'])
    if len(m) == 1:
        m = '0' + m
    if len(t) == 1:
        t = '0' + t
    gebdat = t + '.' + m + '.' + j
    # Layout
    c = canvas.Canvas(saveverzeichnis, pagesize=A4)
    c.setAuthor("UKH")
    c.setTitle(u'Versichertenservice')
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    #####################################################
    # Grauer Hintergrund                                #
    #####################################################
    c.setFillGray(0.85)
    c.rect(1.4 * cm, 0.5 * cm, width=19.0 * cm, height=28.9 * cm, stroke=0, fill=1)
    #####################################################
    # Überschrift                                       #
    #####################################################
    c.setFillColor(black)
    c.setFont(schriftartfett,18)
    c.drawString(1.6 * cm, 28.7 * cm, u"Versichertenservice " + datum)
    #####################################################
    # Titel                                             #
    #####################################################
    c.setFont(schriftartfett, 10)
    c.drawString(1.6 * cm, 27.7 * cm, u'Versicherte Person:')
    #####################################################
    # Name                                              #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(1.6 * cm, 25.2 * cm, width=11.8 * cm, height=1.9 * cm, stroke=1, fill=1)
    c.setFillColor(blue)
    c.setFont(schriftartfett, 21)
    if len(data.ansprechpartner) > 29:
        c.setFont(schriftartfett, 18)
    c.drawString(1.8 * cm, 26.0 * cm, data.ansprechpartner)
    #####################################################
    # Aktenzeichen Daten                                #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(13.7 * cm, 25.2 * cm, width=06.5 * cm, height=4.0 * cm, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont(schriftartfett, 12)
    x1 = 13.9
    y = 28.5
    c.drawString(x1 * cm, y * cm, u"Aktenzeichen - Daten")
    c.setFont(schriftartfett, 11)
    y = y - 0.9
    c.drawString(x1 * cm, y * cm, u"Aktenzeichen")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u"Unfalldatum")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u"Geburtsdatum")
    y = y - 0.5
    c.setFillColor(black)
    c.setFont(schriftart, 12)
    x2 = 16.9
    y = 27.6
    c.drawString(x2 * cm, y * cm, data.az)
    y = y - 0.5
    c.drawString(x2 * cm, y * cm, unfdat)
    y = y - 0.5
    c.drawString(x2 * cm, y * cm, gebdat)
    y = y - 0.5
    #####################################################
    # Info                                              #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(1.6 * cm, 2.0 * cm, width=18.6 * cm, height=21.5 * cm, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont(schriftartfett, 12)
    x1 = 1.9
    y = 22.8
    c.drawString(x1 * cm, y * cm, u"Info vom Versichertenservice:")
    y = y - 1.0
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    c.drawString(x1 * cm, y * cm, u"Der oben genannte Versicherte wurde am " + data.anfragedatum + " zur Teilnahme am Versichertenservice eingeladen.")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, data.anrede + ' ' + data.ansprechpartner + u" hat am " + datum + " die Einladung abgelehnt.")
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, data.anrede + ' ' + data.ansprechpartner + u" wünscht bis auf weiteres eine Schriftliche Kommunikation.")
    #####################################################
    # Datum                                             #
    #####################################################
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    txt = u"Dieses Schreiben wurde am "
    zeit = strftime("%H:%M:%S", localtime())
    c.drawString(x1 * cm, 01.30 * cm, txt + datum + u' um ' + zeit + u' Uhr erstellt')
    # Seitenumbruch
    c.showPage()
    # ENDE und Save
    c.save()


def Zusage_pdf(data, grunddaten):
    # Dateiname
    datum = str(strftime("%d.%m.%Y", localtime()))
    datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
    verzeichnis = getDaleDir()
    dateiname = datum2 + '_' + data.az + '.pdf'
    saveverzeichnis = verzeichnis + '/' + dateiname
    # Grunddaten
    j = str(grunddaten['unfujj'])
    m = str(grunddaten['unfumm'])
    t = str(grunddaten['unfutt'])
    if len(m) == 1:
        m = '0' + m
    if len(t) == 1:
        t = '0' + t
    unfdat = t + '.' + m + '.' + j
    j = str(grunddaten['prsgjj'])
    m = str(grunddaten['prsgmm'])
    t = str(grunddaten['prsgtt'])
    if len(m) == 1:
        m = '0' + m
    if len(t) == 1:
        t = '0' + t
    gebdat = t + '.' + m + '.' + j
    # Layout
    c = canvas.Canvas(saveverzeichnis, pagesize=A4)
    c.setAuthor("UKH")
    c.setTitle(u'Versichertenservice')
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    #####################################################
    # Grauer Hintergrund                                #
    #####################################################
    c.setFillGray(0.85)
    c.rect(1.4 * cm, 0.5 * cm, width=19.0 * cm, height=28.9 * cm, stroke=0, fill=1)
    #####################################################
    # Überschrift                                       #
    #####################################################
    c.setFillColor(black)
    c.setFont(schriftartfett,18)
    c.drawString(1.6 * cm, 28.7 * cm, u"Versichertenservice " + datum)
    #####################################################
    # Titel                                             #
    #####################################################
    c.setFont(schriftartfett, 10)
    c.drawString(1.6 * cm, 27.7 * cm, u'Versicherte Person:')
    #####################################################
    # Name                                              #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(1.6 * cm, 25.2 * cm, width=11.8 * cm, height=1.9 * cm, stroke=1, fill=1)
    c.setFillColor(blue)
    c.setFont(schriftartfett, 21)
    if len(data.ansprechpartner) > 29:
        c.setFont(schriftartfett, 18)
    c.drawString(1.8 * cm, 26.0 * cm, data.ansprechpartner)
    #####################################################
    # Aktenzeichen Daten                                #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(13.7 * cm, 25.2 * cm, width=06.5 * cm, height=4.0 * cm, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont(schriftartfett, 12)
    x1 = 13.9
    y = 28.5
    c.drawString(x1 * cm, y * cm, u"Aktenzeichen - Daten")
    c.setFont(schriftartfett, 11)
    y = y - 0.9
    c.drawString(x1 * cm, y * cm, u"Aktenzeichen")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u"Unfalldatum")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u"Geburtsdatum")
    y = y - 0.5
    c.setFillColor(black)
    c.setFont(schriftart, 12)
    x2 = 16.9
    y = 27.6
    c.drawString(x2 * cm, y * cm, data.az)
    y = y - 0.5
    c.drawString(x2 * cm, y * cm, unfdat)
    y = y - 0.5
    c.drawString(x2 * cm, y * cm, gebdat)
    y = y - 0.5
    #####################################################
    # Info                                              #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(1.6 * cm, 2.0 * cm, width=18.6 * cm, height=21.5 * cm, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont(schriftartfett, 12)
    x1 = 1.9
    x2 = 8
    y = 22.8
    c.drawString(x1 * cm, y * cm, u"Info vom Versichertenservice - Seite 1 von 2:")
    y = y - 1.0
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    c.drawString(x1 * cm, y * cm, u"Der oben genannte Versicherte wurde am " + data.anfragedatum + " zur Teilnahme am Versichertenservice eingeladen.")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, data.anrede + ' ' + data.ansprechpartner + u" hat am " + datum + " die Einladung angenommen und folgendes mitgeteilt:")
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, u'Zustimmung Datenschutzrichtlinien:')
    c.drawString(x2 * cm, y * cm, data.active)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Einwilligung Datenerhebung:')
    c.drawString(x2 * cm, y * cm, data.datenerhebung)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Einwilligung zur Datenübermittlung:')
    c.drawString(x2 * cm, y * cm, data.datenuebermittlung)
    x1 = 1.9
    x2 = 5
    x3 = 10.9
    y = y - 1.5
    c.drawString(x1 * cm, y * cm, u'Die verfügbaren Kontaktdaten wurden gegebenenfalls angepasst, bzw. erweitert:')
    y = y - 1.0
    c.drawString(x2 * cm, y * cm, u'Aktuelle Kontaktdaten:')
    c.drawString(x3 * cm, y * cm, u'Geänderte Kontaktdaten:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, u'Anrede:')
    c.drawString(x2 * cm, y * cm, grunddaten['ikanr'])
    c.drawString(x3 * cm, y * cm, data.anrede)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Vorname:')
    c.drawString(x2 * cm, y * cm, grunddaten['iknam2'])
    c.drawString(x3 * cm, y * cm, data.vname)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Nachname:')
    c.drawString(x2 * cm, y * cm, grunddaten['iknam1'])
    c.drawString(x3 * cm, y * cm, data.nname)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Straße:')
    c.drawString(x2 * cm, y * cm, grunddaten['ikstr'])
    c.drawString(x3 * cm, y * cm, data.vsstr)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Hausnummer:')
    c.drawString(x2 * cm, y * cm, grunddaten['ikhnr'])
    c.drawString(x3 * cm, y * cm, data.vshnr)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Plz, Ort:')
    ikhplz = str(grunddaten['ikhplz'])
    ikhort = grunddaten['ikhort'].strip()
    plzort = ikhplz + ' ' + ikhort
    c.drawString(x2 * cm, y * cm, plzort)
    c.drawString(x3 * cm, y * cm, data.vsplz + ', ' + data.vsort)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Geburtsdatum:')
    T = str(grunddaten['prsgtt']).strip()
    if len(T) == 1:
        T = '0' + T
    M = str(grunddaten['prsgmm']).strip()
    if len(M) == 1:
        M = '0' + M
    J = str(grunddaten['prsgjj']).strip()
    gebdat = T + '.' + M + '.' + J
    c.drawString(x2 * cm, y * cm, gebdat)
    c.drawString(x3 * cm, y * cm, data.gebdat)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Unfalldatum:')
    T = str(grunddaten['unfutt']).strip()
    if len(T) == 1:
        T = '0' + T
    M = str(grunddaten['unfumm']).strip()
    if len(M) == 1:
        M = '0' + M
    J = str(grunddaten['unfujj']).strip()
    unfdat = T + '.' + M + '.' + J
    c.drawString(x2 * cm, y * cm, unfdat)
    c.drawString(x3 * cm, y * cm, data.unfdat)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Vorwahl, Telefon:')
    ikvwhl = str(grunddaten['ikvwhl']).strip()
    iktlnr = str(grunddaten['iktlnr']).strip()
    telefonnummer = ''
    if ikvwhl != '':
        telefonnummer = ikvwhl + ', ' + iktlnr
    c.drawString(x2 * cm, y * cm, telefonnummer)
    c.drawString(x3 * cm, y * cm, data.vsvwl + ', ' + data.vstel)
    y = y - 1.5
    c.drawString(x1 * cm, y * cm, u'Folgende neue Daten wurden von der versicherten Person zur Verfügung gestellt:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, u'E-Mail:')
    c.drawString(x2 * cm, y * cm, data.email)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Arbeitgeber:')
    c.drawString(x2 * cm, y * cm, data.jobinfo1)
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u'Beruf, Tätigkeit:')
    c.drawString(x2 * cm, y * cm, data.jobinfo2)
    #####################################################
    # Datum                                             #
    #####################################################
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    txt = u"Dieses Schreiben wurde am "
    zeit = strftime("%H:%M:%S", localtime())
    c.drawString(x1 * cm, 01.30 * cm, txt + datum + u' um ' + zeit + u' Uhr erstellt')
    #####################################################
    # Seitenumbruch                                     #
    # Seite 2                                           #
    #####################################################
    c.showPage()
    #####################################################
    # Grauer Hintergrund                                #
    #####################################################
    c.setFillGray(0.85)
    c.rect(1.4 * cm, 0.5 * cm, width=19.0 * cm, height=28.9 * cm, stroke=0, fill=1)
    #####################################################
    # Überschrift                                       #
    #####################################################
    c.setFillColor(black)
    c.setFont(schriftartfett,18)
    c.drawString(1.6 * cm, 28.7 * cm, u"Versichertenservice " + datum)
    #####################################################
    # Titel                                             #
    #####################################################
    c.setFont(schriftartfett, 10)
    c.drawString(1.6 * cm, 27.7 * cm, u'Versicherte Person:')
    #####################################################
    # Name                                              #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(1.6 * cm, 25.2 * cm, width=11.8 * cm, height=1.9 * cm, stroke=1, fill=1)
    c.setFillColor(blue)
    c.setFont(schriftartfett, 21)
    if len(data.ansprechpartner) > 29:
        c.setFont(schriftartfett, 18)
    c.drawString(1.8 * cm, 26.0 * cm, data.ansprechpartner)
    #####################################################
    # Aktenzeichen Daten                                #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(13.7 * cm, 25.2 * cm, width=06.5 * cm, height=4.0 * cm, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont(schriftartfett, 12)
    x1 = 13.9
    y = 28.5
    c.drawString(x1 * cm, y * cm, u"Aktenzeichen - Daten")
    c.setFont(schriftartfett, 11)
    y = y - 0.9
    c.drawString(x1 * cm, y * cm, u"Aktenzeichen")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u"Unfalldatum")
    y = y - 0.5
    c.drawString(x1 * cm, y * cm, u"Geburtsdatum")
    y = y - 0.5
    c.setFillColor(black)
    c.setFont(schriftart, 12)
    x2 = 16.9
    y = 27.6
    c.drawString(x2 * cm, y * cm, data.az)
    y = y - 0.5
    c.drawString(x2 * cm, y * cm, unfdat)
    y = y - 0.5
    c.drawString(x2 * cm, y * cm, gebdat)
    y = y - 0.5
    #####################################################
    # Info                                              #
    #####################################################
    c.setLineWidth(0.5)
    c.setFillGray(1.0)
    c.rect(1.6 * cm, 2.0 * cm, width=18.6 * cm, height=21.5 * cm, stroke=1, fill=1)
    c.setFillColor(black)
    c.setFont(schriftartfett, 12)
    x1 = 1.9
    x2 = 5
    y = 22.8
    c.drawString(x1 * cm, y * cm, u"Info vom Versichertenservice - Seite 2 von 2:")
    y = y - 1.0
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    c.drawString(x1 * cm, y * cm, u'Weiterhin wurden folgende Daten von der Versicherten Person zur Verfügung gestellt:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, u'Daten der Krankenkasse:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, data.kkdaten)
    y = y - 2.0
    c.drawString(x1 * cm, y * cm, u'Versichertennummer:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, data.kkvsnummer)
    y = y - 2.0
    c.drawString(x1 * cm, y * cm, u'Hausärztliche Praxis:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, data.hausarzt)
    y = y - 2.0
    c.drawString(x1 * cm, y * cm, u'Weitere Ärztinnen und Ärzte:')
    y = y - 1.0
    c.drawString(x1 * cm, y * cm, data.zusatzarzt)
    #####################################################
    # Datum                                             #
    #####################################################
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    txt = u"Dieses Schreiben wurde am "
    zeit = strftime("%H:%M:%S", localtime())
    c.drawString(x1 * cm, 01.30 * cm, txt + datum + u' um ' + zeit + u' Uhr erstellt')
    # ENDE und Save
    c.save()





