#!/usr/bin/env python                                                                                                                             
# -*- coding: utf-8 -*-

import os
import datetime


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue
from time import localtime, strftime

bcp = '/'.join(__file__.split('/')[:-2])


def pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum):
    c.setFillColor(black)
    c.setFont(schriftartfett, 10)
    c.drawString(2.2 * cm, 28.5 * cm, u"Rehabilitation")
    c.drawString(2.2 * cm, 28.0 * cm, u"und Entschädigung")
    logo = bcp + '/adhoc/static/logo_ukh.JPG'
    c.drawImage(logo, 14.2 * cm, 27.7 * cm, width=4.5 * cm, height=1.3 * cm)
    c.setFont(schriftart, 8)
    t1 = u"Dieses Formular wurde über den Online-Service der Unfallkasse Hessen erstellt und versandt und trägt daher keine Unterschrift."
    c.drawString(2.2 * cm, 1.5 * cm, t1)
    return c


def Absage_pdf(data, grunddaten):
    seite = 1
    zeit = strftime("%H:%M:%S", localtime())
    datum = str(strftime("%d.%m.%Y", localtime()))
    datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
    # Datei Name Verzeichnis
    verzeichnis = '/ausgang/fax133a'
    dateiname = datum2 + '_' + data.az + '.pdf'
    saveverzeichnis = verzeichnis + '/' + dateiname
    # Layout
    c = canvas.Canvas(saveverzeichnis, pagesize=A4)
    c.setAuthor("UKH")
    c.setTitle(u'Druckversion')
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    # Seite 1
    c = pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum)
    # Absender
    y1 = 26.5
    x1 = 11.7
    x2 = 15.5
    # Daten
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
    c.setFont(schriftartfett, 10)
    #c.drawString(2.2 * cm, y1 * cm, u"Seite: " + str(seite))
    c.drawString(x1 * cm, y1 * cm, u"Aktenzeichen:")
    c.drawString(x2 * cm, y1 * cm, data.az)
    y1 = y1 - 0.5
    c.drawString(x1 * cm, y1 * cm, u"Versicherte Person:")
    c.drawString(x2 * cm, y1 * cm, data.ansprechpartner)
    y1 = y1 - 0.5
    c.drawString(x1 * cm, y1 * cm, u"Unfalldatum:")
    c.drawString(x2 * cm, y1 * cm, unfdat)
    y1 = y1 - 0.5
    c.drawString(x1 * cm, y1 * cm, u"Geburtsdatum:")
    c.drawString(x2 * cm, y1 * cm, gebdat)
    y1 = y1 - 1.0
    c.drawString(x1 * cm, y1 * cm, u"Datum:")
    c.drawString(x2 * cm, y1 * cm, datum)
    y1 = y1 - 0.5
    c.drawString(x1 * cm, y1 * cm, u"Uhrzeit:")
    c.drawString(x2 * cm, y1 * cm, zeit)
    # Empfänger
    y1 = 24.0
    x1 = 2.2
    c.setFont(schriftartfett, 12)
    c.drawString(x1 * cm, y1 * cm, u"Unfallkasse Hessen")
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, u"Leonardo-da-Vinci-Allee 20")
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"60486 Frankfurt am Main")
    # Info
    c.setFillColor(black)
    c.setFont(schriftartfett,16)
    c.drawString(2.2 * cm, 20 * cm, u"Versichertenservice " + datum)
    # Daten
    y1 = 19.0
    c.setFont(schriftartfett, 10)
    t1 = u"Der oben genannte Versicherte wurde am "
    t2 = u" zur Teilnahme am Versichertenservice eingeladen."
    c.drawString(x1 * cm, y1 * cm, t1 + data.anfragedatum + t2)
    y1 = y1 - 1.0
    c.drawString(x1 * cm, y1 * cm, data.anrede + ' ' + data.ansprechpartner + u" hat am " + datum + " die Einladung abgelehnt.")
    y1 = y1 - 1.0
    c.drawString(x1 * cm, y1 * cm, data.anrede + ' ' + data.ansprechpartner + u" wünscht bis auf weiteres eine Schriftliche Kommunikation.")
    # Seitenumbruch
    c.showPage()
    # ENDE und Save
    c.save()


def Zusage_pdf(data, grunddaten):
    seite = 1
    zeit = strftime("%H:%M:%S", localtime())
    datum = str(strftime("%d.%m.%Y", localtime()))
    datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
    # Datei Name Verzeichnis
    verzeichnis = '/ausgang/fax133a'
    dateiname = datum2 + '_' + data.az + '.pdf'
    saveverzeichnis = verzeichnis + '/' + dateiname
    # Layout
    c = canvas.Canvas(saveverzeichnis, pagesize=A4)
    c.setAuthor("UKH")
    c.setTitle(u'Druckversion')
    schriftart = "Helvetica"
    schriftartfett = "Helvetica-Bold"
    # Seite 1
    c = pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum)
    # Absender
    y1 = 26.5
    x1 = 11.7
    x2 = 15.5
    # Daten
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
    c.setFont(schriftartfett, 10)
    c.drawString(2.2 * cm, y1 * cm, u"Seite: " + str(seite))
    c.drawString(x1 * cm, y1 * cm, u"Aktenzeichen:")
    c.drawString(x2 * cm, y1 * cm, data.az)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"Versicherte Person:")
    c.drawString(x2 * cm, y1 * cm, data.ansprechpartner)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"Unfalldatum:")
    c.drawString(x2 * cm, y1 * cm, unfdat)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"Geburtsdatum:")
    c.drawString(x2 * cm, y1 * cm, gebdat)
    y1 -= 1.0 
    c.drawString(x1 * cm, y1 * cm, u"Datum:")
    c.drawString(x2 * cm, y1 * cm, datum)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"Uhrzeit:")
    c.drawString(x2 * cm, y1 * cm, zeit)
    # Empfänger
    y1 = 24.0
    x1 = 2.2
    x2 = 9.5 
    c.setFont(schriftartfett, 12)
    c.drawString(x1 * cm, y1 * cm, u"Unfallkasse Hessen")
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, u"Leonardo-da-Vinci-Allee 20")
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u"60486 Frankfurt am Main")
    # Info
    c.setFillColor(black)
    c.setFont(schriftartfett,16)
    c.drawString(2.2 * cm, 20 * cm, u"Versichertenservice " + datum)
    # Daten
    y1 = 19.0
    c.setFont(schriftartfett, 10)
    t1 = u"Der oben genannte Versicherte wurde am "
    t2 = u" zur Teilnahme am Versichertenservice eingeladen."
    c.drawString(x1 * cm, y1 * cm, t1 + data.anfragedatum + t2)
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, data.anrede + ' ' + data.ansprechpartner + u" hat am " + datum + " die Einladung angenommen und folgendes mitgeteilt:")
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, u'Zustimmung Datenschutzrichtlinien:')
    c.drawString(x2 * cm, y1 * cm, data.active)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Einwilligung Datenerhebung:')
    c.drawString(x2 * cm, y1 * cm, data.datenerhebung)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Einwilligung zur Datenübermittlung:')
    c.drawString(x2 * cm, y1 * cm, data.datenuebermittlung)
    x2 = 6
    x3 = 11.9
    y1 -= 1.5
    c.drawString(x1 * cm, y1 * cm, u'Die verfügbaren Kontaktdaten wurden gegebenenfalls angepasst, bzw. erweitert:')
    y1 -= 1.0
    c.drawString(x2 * cm, y1 * cm, u'Aktuelle Kontaktdaten:')
    c.drawString(x3 * cm, y1 * cm, u'Geänderte Kontaktdaten:')
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, u'Anrede:')
    c.drawString(x2 * cm, y1 * cm, grunddaten['ikanr'])
    c.drawString(x3 * cm, y1 * cm, data.anrede)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Vorname:')
    c.drawString(x2 * cm, y1 * cm, grunddaten['iknam2'])
    c.drawString(x3 * cm, y1 * cm, data.vname)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Nachname:')
    c.drawString(x2 * cm, y1 * cm, grunddaten['iknam1'])
    c.drawString(x3 * cm, y1 * cm, data.nname)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Straße:')
    c.drawString(x2 * cm, y1 * cm, grunddaten['ikstr'])
    c.drawString(x3 * cm, y1 * cm, data.vsstr)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Hausnummer:')
    c.drawString(x2 * cm, y1 * cm, grunddaten['ikhnr'])
    c.drawString(x3 * cm, y1 * cm, data.vshnr)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Plz, Ort:')
    ikhplz = str(grunddaten['ikhplz'])
    ikhort = grunddaten['ikhort'].strip()
    plzort = ikhplz + ' ' + ikhort
    c.drawString(x2 * cm, y1 * cm, plzort)
    c.drawString(x3 * cm, y1 * cm, data.vsplz + ', ' + data.vsort)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Geburtsdatum:')
    T = str(grunddaten['prsgtt']).strip()
    if len(T) == 1:
        T = '0' + T
    M = str(grunddaten['prsgmm']).strip()
    if len(M) == 1:
        M = '0' + M
    J = str(grunddaten['prsgjj']).strip()
    gebdat = T + '.' + M + '.' + J
    c.drawString(x2 * cm, y1 * cm, gebdat)
    c.drawString(x3 * cm, y1 * cm, data.gebdat)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Unfalldatum:')
    T = str(grunddaten['unfutt']).strip()
    if len(T) == 1:
        T = '0' + T
    M = str(grunddaten['unfumm']).strip()
    if len(M) == 1:
        M = '0' + M
    J = str(grunddaten['unfujj']).strip()
    unfdat = T + '.' + M + '.' + J
    c.drawString(x2 * cm, y1 * cm, unfdat)
    c.drawString(x3 * cm, y1 * cm, data.unfdat)
    y1 -= 0.5
    c.drawString(x1 * cm, y1 * cm, u'Vorwahl, Telefon:')
    ikvwhl = str(grunddaten['ikvwhl']).strip()
    iktlnr = str(grunddaten['iktlnr']).strip()
    telefonnummer = ''
    if ikvwhl != '':
        telefonnummer = ikvwhl + ', ' + iktlnr
    c.drawString(x2 * cm, y1 * cm, telefonnummer)
    c.drawString(x3 * cm, y1 * cm, data.vsvwl + ', ' + data.vstel)
    y1 -= 1.5
    c.drawString(x1 * cm, y1 * cm, u'Folgende neue Daten wurden von der versicherten Person zur Verfügung gestellt:')
    y1 -= 1.0
    c.drawString(x1 * cm, y1 * cm, u'E-Mail:')
    c.drawString(x2 * cm, y1 * cm, data.email)
    y1 -= 0.5
    #####################################################
    # Seitenumbruch                                     #
    # Seite 2                                           #
    #####################################################
    c.showPage()
    c = pdf_seitenkopf(data, saveverzeichnis, c, schriftart, schriftartfett, datum)
    c.setFont(schriftartfett, 10)
    seite += 1
    y1 = 26.5
    x1 = 2.2
    x3 = 2.7
    c.drawString(2.2 * cm, y1 * cm, u"Seite: " + str(seite))
    y1 -= 1.0
    c.setFillColor(black)
    c.setFont(schriftartfett, 10)
    c.drawString(x1 * cm, y1 * cm, u'Weiterhin wurden folgende Daten von der Versicherten Person zur Verfügung gestellt:')
    y1 -= 1.5
    c.drawString(x1 * cm, y1 * cm, u'Arbeitgeber:')
    y1 -= 0.5
    text = cutrow(data.jobinfo1, 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x3 * cm, y1 * cm, text[z1])
        z1 += 1
    y1 -= 2.5
    c.setFont(schriftartfett, 10)
    c.drawString(x1 * cm, y1 * cm, u'Beruf, Tätigkeit:')
    y1 -= 0.5
    text = cutrow(data.jobinfo2, 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x3 * cm, y1 * cm, text[z1])
        z1 += 1
    y1 -= 2.5
    c.setFont(schriftartfett, 10)
    c.drawString(x1 * cm, y1 * cm, u'Daten der Krankenkasse:')
    y1 -= 0.5
    text = cutrow(data.kkdaten, 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x3 * cm, y1 * cm, text[z1])
        z1 += 1
    y1 -= 2.5
    c.setFont(schriftartfett, 10)
    c.drawString(x1 * cm, y1 * cm, u'Versichertennummer:')
    y1 -= 0.5
    text = cutrow(data.kkvsnummer, 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x3 * cm, y1 * cm, text[z1])
        z1 += 1
    y1 -= 2.5
    c.setFont(schriftartfett, 10)
    c.drawString(x1 * cm, y1 * cm, u'Hausärztliche Praxis:')
    y1 -= 0.5
    text = cutrow(data.hausarzt, 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x3 * cm, y1 * cm, text[z1])
        z1 += 1
    y1 -= 2.5
    c.setFont(schriftartfett, 10)
    c.drawString(x1 * cm, y1 * cm, u'Weitere Ärztinnen und Ärzte:')
    y1 -= 0.5
    text = cutrow(data.zusatzarzt, 100)
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x3 * cm, y1 * cm, text[z1])
        z1 += 1
    # ENDE und Save
    c.save()


def cutrow(text, ende=100, maxrows=20, maxstring=3000):
    text = text.replace("<br />", "\n")
    text = text.replace("<p>", "")
    text = text.replace("</p>", "")
    text = text.replace("<ul>", "")
    text = text.replace("</ul>", "")
    text = text.replace("<ol>", "")
    text = text.replace("</ol>", "")
    text = text.replace("<li>", "  - ")
    text = text.replace("</li>", "")
    text = text.replace('<span style="text-decoration: underline;">', '')
    text = text.replace('</span>', '')
    text = text.replace('<em>', '')
    text = text.replace('</em>', '')
    text = text.replace('<p style="text-align: left;">', '')
    text = text.replace('<p style="text-align: center;">', '')
    text = text.replace('<p style="text-align: right;">', '')
    text = text.replace('<strong>', '')
    text = text.replace('</strong>', '')
    text = text.replace('<span style="font-size: 10px;">', '')
    text = text.replace('<span style="font-size: 12px;">', '')
    text = text.replace('<span style="font-size: 13px;">', '')
    text = text.replace('<span style="font-size: 14px;">', '')
    text = text.replace('<span style="font-size: 16px;">', '')
    text = text.replace('<span style="font-size: 18px;">', '')
    text = text.replace('<span style="font-size: 20px;">', '')
    text = text.replace("\t", "     ")
    text = text.replace("\r", " ")
    start = 0
    konstante = ende
    druckliste = []
    laenge = len(text) / 5
    if laenge == 0:
        laenge = 1
    for x in range(laenge):
        if start != -1:
            textteil = text[start:ende]
            # Klaerung, ob bereits Umbrueche vorhanden sind
            umbruch = textteil.find("\n")
            # Wenn nein, Einbau eines Umbruches
            if umbruch == -1:
                if textteil > ' ':
                    if len(textteil) < konstante:
                        druckliste.append(textteil)
                        zeilenende = konstante
                    else:
                        zeilenende = textteil.rfind(' ')
                        druckliste.append(textteil[:zeilenende])

                    # Wenn kein anderer Text mehr kommt - Abbruch
                    if start == start + zeilenende + 1:
                        start = -1
                    else:
                        start = start + zeilenende + 1
                        ende = start + konstante
            # Wenn ja, dann weiter mit dem naechsten Textteil
            else:
                druckliste.append(textteil[:umbruch])

                # Wenn kein neuer Text mehr kommt - Abbruch
                if start == start + umbruch + 1:
                    start = -1
                else:
                    start = start + umbruch + 1
                    ende = start + konstante
    return druckliste





########### ALT LÖSCHEN !!!! #############


def Zusage_ALT_pdf(data, grunddaten):
    # Dateiname
    datum = str(strftime("%d.%m.%Y", localtime()))
    datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
    verzeichnis = '/ausgang/fax133a'
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
