# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite

from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from uvc.letterbasket.interfaces import ILetterBasket, IMessage
from uvc.letterbasket.views import AddThread, AddMessage
from uvc.letterbasket.views import ThreadDisplay as ThreadIndex
from uvc.letterbasket.views import MessageDisplay as MessageIndex
from uvc.letterbasket.resources import threadcss
from ukhtheme.grok.layout import ILayer
from zope.interface import directlyProvides
from ..interfaces import IQuestion, IAnswer
from .workflow import MessageState

grok.templatedir('templates')


class NachrichtenLP(uvcsite.Page):
    grok.context(ILetterBasket)
    grok.name('index')


class StartThread(AddThread):
    grok.layer(ILayer)

    def create(self, data):
        content = AddThread.create(self, data)
        directlyProvides(content, IQuestion)
        return content

    def add(self, content):
        AddThread.add(self, content)


def letter_is_sent(form):
    return IWorkflowState(form.context).getState() == MessageState.sent


def letter_is_read(form):
    return IWorkflowState(form.context).getState() == MessageState.read


class Reply(AddMessage):
    grok.name('add')
    grok.layer(ILayer)

    def create(self, data):
        content = AddMessage.create(self, data)
        directlyProvides(content, IAnswer)
        return content

    def add(self, content):
        AddMessage.add(self, content)
        IWorkflowInfo(self.context).fireTransition('reply')

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
        self.redirect(self.url(self.context))


class MessageDisplay(MessageIndex):
    grok.name('display')
    grok.context(IMessage)
    grok.require('zope.Public')
    grok.layer(ILayer)

    def actions(self):
        uri = self.url(self.context)
        if IQuestion.providedBy(self.context):
            if letter_is_sent(self):
                yield {
                    'title': 'Mark as read',
                    'url': '%s/mark_as_read' % uri
                }
            elif letter_is_read(self):
                yield {
                    'title': 'Antworten',
                    'url': '%s/add' % uri
                }
        attachment = getattr(self.context, 'attachment', None)
        if attachment is not None:
            yield {
                'title': 'Anhang herunterladen',
                'url': "%s/++download++attachment" % uri
            }
