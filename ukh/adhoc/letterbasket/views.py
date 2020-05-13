# -*- coding: utf-8 -*-
# # Copyright (c) 2007-2019 NovaReto GmbH
# # cklinger@novareto.de


import grok
import uvcsite

from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from uvc.letterbasket.interfaces import ILetterBasket
from uvc.letterbasket.views import AddThread, AddMessage
from uvc.letterbasket.views import ThreadDisplay as ThreadIndex
from uvc.letterbasket.views import MessageDisplay as MessageIndex
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


class ThreadDisplay(ThreadIndex):
    grok.name('index')
    grok.context(IQuestion)
    grok.layer(ILayer)

    def update(self):
        ThreadIndex.update(self)
        self.can_answer = IWorkflowState(self.context) in (
            MessageState.sent, MessageState.read)


class MessageDisplay(MessageIndex):
    grok.name('display')
    grok.context(IAnswer)
    grok.require('zope.Public')

    can_answer = False
