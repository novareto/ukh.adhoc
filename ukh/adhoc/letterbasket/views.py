# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de

import pytz
import grok
import uvcsite

from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from uvc.letterbasket.interfaces import ILetterBasket, IMessage
from uvc.letterbasket.views import AddThread, AddMessage, ThreadInfo
from uvc.letterbasket.views import ThreadDisplay as ThreadIndex
from uvc.letterbasket.views import MessageDisplay as MessageIndex
from uvc.letterbasket.resources import threadcss
from ukhtheme.grok.layout import ILayer
from zope.interface import directlyProvides
from ..interfaces import IQuestion, IAnswer
from ..resources import lb_badge_css
from .workflow import MessageState, titleForState
from zeam.form.base.markers import HIDDEN
from zope.interface import Interface, implementer


tz = pytz.timezone("Europe/Berlin")


class IMessageTableItem(Interface):
    pass


@implementer(IMessageTableItem)
class MessageTableItem(grok.Adapter):
    grok.context(IQuestion)

    def title(self):
        return self.context.title

    def getState(self):
        return IWorkflowState(self.context).getState().name

    def state(self):
        if self.context.principal.id == 'zope.anybody':
            if titleForState(self.getState()) == 'gesendet':
                if self.hasAnswer() is None:
                    return 'ungelesen'
        if self.context.principal.id != 'zope.anybody':
            if self.hasAnswer() == 'sent':
                if titleForState(self.getState()) == 'gesendet':
                    return 'antwort'
            if self.hasAnswer() == 'read':
                if titleForState(self.getState()) == 'gesendet':
                    return 'antwort gelesen'
        return titleForState(self.getState())

    def date(self):
        return self.context.modtime.astimezone(tz).strftime('%d.%m.%Y %H:%M')

    def author(self):
        def p_name(context):
            principal = context.principal.id
            if principal == 'zope.anybody':
                principal = getattr(self.context, 'sachbearbeiter', 'UKH-Sachbearbeiter')
            return principal
        principal = p_name(self.context)
        if len(self.context) > 0:
            answer = [x for x in self.context.values()][0]
            principal += " / %s" % p_name(answer)
        return principal

    def hasAnswer(self):
        if len(self.context) > 0:
            answer = [x for x in self.context.values()][0]
            return IWorkflowState(answer).getState().name
        return None

    def css_class(self):
        offen = "glyphicon glyphicon-envelope"
        fertig = "glyphicon glyphicon-ok"
        answered = "glyphicon glyphicon-pencil"
        if self.hasAnswer() in ('read', 'finish'):
            return fertig
        if self.getState() == 'read':
            return fertig
        if self.getState() == 'replied':
            return answered
        if self.context.principal.id != 'zope.anybody':
            if self.getState() == 'sent':
                if self.hasAnswer() is None:
                    return answered
                if self.hasAnswer() == 'sent':
                    return offen
        return offen

grok.templatedir('templates')


class NachrichtenLP(uvcsite.Page):
    grok.context(ILetterBasket)
    grok.name('index')

    def nachrichten(self):
        nachrichten = self.context.values()
        nachrichten = sorted(nachrichten, key=lambda nachricht: nachricht.modtime, reverse = True)
        for nachricht in nachrichten:
            yield IMessageTableItem(nachricht)

    def update(self):
        lb_badge_css.need()

    def tfs(self, state):
        return titleForState(state.value)


class StartThread(AddThread):
    grok.layer(ILayer)
    description = u''

    @property
    def fields(self):
        fields = super(StartThread, self).fields
        fields['attachment'].mode = HIDDEN
        fields['doc_id'].mode = HIDDEN
        fields['title'].description = u""
        fields['message'].description = u""
        return fields

    def create(self, data):
        content = AddThread.create(self, data)
        directlyProvides(content, IQuestion)
        return content

    def add(self, content):
        AddThread.add(self, content)


def by_ukh(form):
    if form.context.principal.id == 'zope.anybody':
        return True
    return False


def letter_is_sent(form):
    return IWorkflowState(form.context).getState() == MessageState.sent


def letter_is_read(form):
    return IWorkflowState(form.context).getState() == MessageState.read


class Reply(AddMessage):
    grok.name('add')
    grok.layer(ILayer)
    description = u''

    @property
    def fields(self):
        fields = super(Reply, self).fields
        fields['attachment'].mode = HIDDEN
        fields['doc_id'].mode = HIDDEN
        fields['title'].description = u""
        fields['message'].description = u""
        fields['title'].mode = "hiddendisplay"
        fields['title'].defaultValue = self.context.title
        return fields

    def create(self, data):
        content = AddMessage.create(self, data)
        directlyProvides(content, IAnswer)
        return content

    def add(self, content):
        AddMessage.add(self, content)
        IWorkflowInfo(self.context).fireTransition('reply')
        #IWorkflowInfo(self.context).fireTransition('finish_reply')

    @uvcsite.action(
        u'Nachricht senden',
        identifier="uvcsite.add", available=letter_is_read)
    def handleAdd(self):
        return AddMessage.handleAdd(self)


class MarkAsRead(grok.View):
    grok.name('mark_as_read')
    grok.context(IQuestion)
    grok.layer(ILayer)

    def update(self):
        if self.request.method != 'POST':
            raise NotImplementedError('This method is only allowed in POST')
        IWorkflowInfo(self.context).fireTransition('read')

    def render(self):
        if self.request.get('QUERY_STRING') == 'answer=True':
            self.redirect(self.url(self.context, 'add'))
        else:
            self.redirect(self.url(self.context.__parent__))


class MarkAsReadAnswer(grok.View):
    grok.name('mark_as_read')
    grok.context(IAnswer)
    grok.layer(ILayer)

    def update(self):
        if self.request.method != 'POST':
            raise NotImplementedError('This method is only allowed in POST')
        IWorkflowInfo(self.context).fireTransition('read')

    def render(self):
        self.redirect(self.url(self.context.__parent__.__parent__))


class MessageDisplay(MessageIndex):
    grok.name('display')
    grok.context(IMessage)
    grok.require('zope.Public')
    grok.layer(ILayer)

    def actions(self):
        uri = self.url(self.context)
        res = []
        if IQuestion.providedBy(self.context):
            if letter_is_sent(self) and by_ukh(self):
                res.append({
                    'title': u'Antworten',
                    'url': '%s/mark_as_read?answer=True' % uri
                })
                res.append({
                    'title': u'Gelesen und zurück',
                    'url': '%s/mark_as_read' % uri
                })
            elif letter_is_read(self):
                res.append({
                    'title': u'Antworten',
                    'url': '%s/add' % uri
                })
        if IAnswer.providedBy(self.context):
            if letter_is_sent(self) and by_ukh(self):
                res.append(
                {
                    'title': u'Gelesen und zurück',
                    'url': '%s/mark_as_read' % uri
                })
        attachment = getattr(self.context, 'attachment', None)
        if attachment is not None:
            res.append({
                'title': u'Anhang herunterladen',
                'url': "%s/++download++attachment" % uri
            })
            #if letter_is_sent(self) and by_ukh(self):
            #    res.append({
            #        'title': u'Anhang herunterladen',
            #        'url': "%s/++download++attachment" % uri
            #    })
        return res


class ThreadInfo(grok.Viewlet):
    grok.order(600)
    grok.context(IMessage)
    grok.require('uvc.AddContent')
    grok.view(uvcsite.AddForm)
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.layer(ILayer)

    @property
    def daten(self):
        return self.context
