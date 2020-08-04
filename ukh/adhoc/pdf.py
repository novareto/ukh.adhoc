#!/usr/bin/env python                                                                                                                             
# -*- coding: utf-8 -*-

import os
import datetime

from ukh.adhoc.interfaces import IAccount
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import black, blue
from time import localtime, strftime
import datetime

bcp = '/'.join(__file__.split('/')[:-2])


def pdf_seitenkopf_master(c, schriftart, schriftartfett, seite):
    c.setFillColor(black)
    c.setFont(schriftartfett, 16)
    c.drawString(2.2 * cm, 28.5 * cm, u"Versichertenportal")
    c.setFont(schriftartfett, 10)
    c.drawString(18 * cm, 2.0 * cm, u"Seite " + str(seite))
    logo = bcp + '/adhoc/static/logo_ukh.JPG'
    c.drawImage(logo, 14.2 * cm, 27.7 * cm, width=4.5 * cm, height=1.3 * cm)
    c.setFont(schriftart, 8)
    t1 = u"Dieses Formular wurde über das Versichertenportal der Unfallkasse "
    t2 = u"Hessen erstellt und versandt und trägt daher keine Unterschrift."
    c.drawString(2.2 * cm, 1.5 * cm, t1 + t2)
    return c


def ueberschrift(c, schriftartfett, text, x1, y1, groesse):
    c.setFont(schriftartfett, groesse)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x1 * cm, y1 * cm, text[z1])
        z1 += 1
    return y1


def antwort(c, schriftart, text, x1, y1):
    c.setFillColor(black)
    c.setFont(schriftart, 10)
    z1 = 0
    for i in text:
        y1 -= 0.4
        c.drawString(x1 * cm, y1 * cm, text[z1])
        z1 += 1
    y1 -= 1.0
    return y1


def cutrow(text, ende=100, maxrows=20, maxstring=3000):
    if text is None:
        return ''
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


def Antwort_pdf(data, grunddaten, status):
    ft = 90
    bt = 90
    gdat = "%s.%s.%s" %(str(grunddaten['prsgtt']).zfill(2), str(grunddaten['prsgmm']).zfill(2), str(grunddaten['prsgjj']))
    today = datetime.date.today()
    tag, monat, jahr = gdat.split('.')
    born = datetime.date(int(jahr), int(monat), int(tag))
    alter = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    zeit = strftime("%H:%M:%S", localtime())
    datum = str(strftime("%d.%m.%Y", localtime()))
    uhrzeit = str(strftime("%H:%M", localtime()))
    datum2 = str(strftime("%Y_%m_%d_%H_%M", localtime()))
    verzeichnis = '/ausgang/fax133a'
    dateiname = datum2 + '_' + data.az + '.pdf'
    saveverzeichnis = verzeichnis + '/' + dateiname
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
    c.drawString(x2 * cm, y1 * cm, data.az)
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Name:")
    c.drawString(x2 * cm, y1 * cm, grunddaten['iknam1'])
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Vorname:")
    c.drawString(x2 * cm, y1 * cm, grunddaten['iknam2'])
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Formular Typ:")
    c.drawString(x2 * cm, y1 * cm, u"Erstanmeldung")
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Formular Bezeichnung:")
    c.drawString(x2 * cm, y1 * cm, u"Erstanmeldung")
    y1 -= 0.6
    c.drawString(x1 * cm, y1 * cm, u"Eingangsdatum, Uhrzeit:")
    c.drawString(x2 * cm, y1 * cm, datum + ', ' + zeit)
    # ----------------------------------------------
    y1 -= 3.0
    c.setFont(schriftartfett, 10)
    if status == 'absage':
        c.drawString(x1 * cm, y1 * cm, u"Die Einladung vom " + data.anfragedatum + u" zum Versichertenportal wurde abgelehnt.")
        y1 = y1 - 1.0
        c.drawString(x1 * cm, y1 * cm, data.anrede + ' ' + data.ansprechpartner + u" wünscht bis auf weiteres eine Schriftliche Kommunikation.")
        # Seitenumbruch
        c.showPage()
        # ENDE und Save
        c.save()
    else:
        x2 = 15.5
        c.drawString(x1 * cm, y1 * cm, u"Die Einladung vom " + data.anfragedatum + u" zum Versichertenportal wurde angenommen.")
        y1 -= 1.0
        c.drawString(x1 * cm, y1 * cm, u"Teilnahme am Versichertenportal und Zustimmung Datenschutzrichtlinien:")
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
        c.drawString(x1 * cm, y1 * cm, u'Die vorhandenen Kontaktdaten wurden überprüft und angepasst/erweitert:')
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
        neuetelefonnummer = ''
        if data.vsvwl != '':
            neuetelefonnummer = data.vsvwl + ', ' + data.vstel
        c.drawString(x2 * cm, y1 * cm, telefonnummer)
        c.drawString(x3 * cm, y1 * cm, neuetelefonnummer)
        y1 -= 0.5
        c.drawString(x1 * cm, y1 * cm, u'E-Mail:')
        c.drawString(x3 * cm, y1 * cm, data.email)
        y1 -= 0.5
        #####################################################
        # Seitenumbruch                                     #
        # Seite 2                                           #
        #####################################################
        c.showPage()
        seite += 1
        c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
        y1 = 26.5
        x1 = 2.2
        x3 = 2.7
        c.setFillColor(black)
        c.setFont(schriftartfett, 10)
        c.drawString(x1 * cm, y1 * cm, u'Folgende Daten von der Versicherten Person zur Verfügung gestellt:')
        y1 -= 1.5
        # ####################################################################
        text = cutrow(data.jobinfo1, 100)
        # Platzbedarf ermitteln
        lt = len(text) * 0.4
        lt += 4
        # ----------------------------------------------
        # Gegebenenfalls Seitenwechsel einleiten
        if lt > y1:
            c.showPage()
            seite += 1
            c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
            y1 = 26.5
        # ----------------------------------------------
        if alter >= 15:
            ftext = cutrow(IAccount.get('jobinfo1').title, ft)
            btext = cutrow(IAccount.get('jobinfo1').description, bt)
        else:
            t1 = u'Unfallbetrieb'
            t2 = u'Bitte nennen Sie uns den Namen und die Anschrift der Kindertagesstätte / des Kindergartens / der Schule'
            ftext = cutrow(t1, ft)
            btext = cutrow(t2, bt)
        y1 = ueberschrift(c, schriftartfett, ftext, x1, y1, 11)
        y1 = ueberschrift(c, schriftartfett, btext, x1, y1, 9)
        y1 -= 0.4
        y1 = antwort(c, schriftart, text, x1, y1)
        # ####################################################################
        text = cutrow(data.jobinfo2, 100)
        # Platzbedarf ermitteln
        lt = len(text) * 0.4
        lt += 4
        # ----------------------------------------------
        # Gegebenenfalls Seitenwechsel einleiten
        if lt > y1:
            c.showPage()
            seite += 1
            c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
            y1 = 26.5
        # ----------------------------------------------
        if alter >= 15:
            ftext = cutrow(IAccount.get('jobinfo2').title, ft)
            btext = cutrow(IAccount.get('jobinfo2').description, bt)
        else:
            t1 = u'Unfallbringende Tätigkeit'
            t2 = u'Bitte beschreiben Sie, bei welcher Tätigkeit sich der Unfall ereignete'
            ftext = cutrow(t1, ft)
            btext = cutrow(t2, bt)
        y1 = ueberschrift(c, schriftartfett, ftext, x1, y1, 11)
        y1 = ueberschrift(c, schriftartfett, btext, x1, y1, 9)
        y1 -= 0.4
        y1 = antwort(c, schriftart, text, x1, y1)
        # ####################################################################
        text = cutrow(data.kkdaten, 100)
        # Platzbedarf ermitteln
        lt = len(text) * 0.4
        lt += 4
        # ----------------------------------------------
        # Gegebenenfalls Seitenwechsel einleiten
        if lt > y1:
            c.showPage()
            seite += 1
            c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
            y1 = 26.5
        # ----------------------------------------------
        if alter >= 15:
            ftext = cutrow(IAccount.get('kkdaten').title, ft)
            btext = cutrow(IAccount.get('kkdaten').description, bt)
        else:
            t1 = u'Krankenkasse Ihres Kindes'
            ftext = cutrow(t1, ft)
            btext = cutrow(IAccount.get('kkdaten').description, bt)
        y1 = ueberschrift(c, schriftartfett, ftext, x1, y1, 11)
        y1 = ueberschrift(c, schriftartfett, btext, x1, y1, 9)
        y1 -= 0.4
        y1 = antwort(c, schriftart, text, x1, y1)
        # ####################################################################
        text = cutrow(data.hausarzt, 100)
        # Platzbedarf ermitteln
        lt = len(text) * 0.4
        lt += 4
        # ----------------------------------------------
        # Gegebenenfalls Seitenwechsel einleiten
        if lt > y1:
            c.showPage()
            seite += 1
            c = pdf_seitenkopf_master(c, schriftart, schriftartfett, seite)
            y1 = 26.5
        # ----------------------------------------------
        if alter >= 15:
            ftext = cutrow(IAccount.get('hausarzt').title, ft)
            btext = cutrow(IAccount.get('hausarzt').description, bt)
        else:
            t1 = u'Kinder-/Hausärztin oder Kinder-/Hausarzt'
            t2 = u'Bitte nennen Sie uns den Namen und die Anschrift der Kinder-/Hausärztin oder des Kinder-/Hausarztes'
            ftext = cutrow(t1, ft)
            btext = cutrow(t2, bt)
        y1 = ueberschrift(c, schriftartfett, ftext, x1, y1, 11)
        y1 = ueberschrift(c, schriftartfett, btext, x1, y1, 9)
        y1 -= 0.4
        y1 = antwort(c, schriftart, text, x1, y1)
        # Seitenumbruch
        c.showPage()
        # ENDE und Save
        c.save()
