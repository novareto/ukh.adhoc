import grok
import enum
import uvc.letterbasket.interfaces
from hurry.workflow import workflow



class MessageState(enum.Enum):
    created = 'created'
    sent = 'sent'
    read = 'read'
    replied = 'replied'
    progress = 'progress'
    finish = 'finish'


MessageWorkflow = workflow.Workflow([

    workflow.Transition(
        transition_id='create',
        title='Created',
        source=None,
        destination=MessageState.created),

    workflow.Transition(
        transition_id='sent',
        title='Sent',
        source=MessageState.created,
        destination=MessageState.sent),

    workflow.Transition(
        transition_id='read',
        title='Read',
        source=MessageState.sent,
        destination=MessageState.read),

    workflow.Transition(
        transition_id='reply',
        title='Reply',
        source=MessageState.read,
        destination=MessageState.replied),

    workflow.Transition(
        transition_id='progress',
        title='Progress',
        source=MessageState.sent,
        destination=MessageState.progress),

    workflow.Transition(
        transition_id='finish',
        title='Finish',
        source=None,
        destination=MessageState.finish)

])


grok.global_utility(
    MessageWorkflow, provides=workflow.IWorkflow,
    name="message", direct=True)


class WorkflowState(workflow.WorkflowState, grok.Adapter):
    grok.context(uvc.letterbasket.interfaces.IMessage)
    grok.provides(workflow.IWorkflowState)
    grok.name('message')


class WorkflowInfo(workflow.WorkflowInfo, grok.Adapter):
    grok.context(uvc.letterbasket.interfaces.IMessage)
    grok.provides(workflow.IWorkflowInfo)
    name = "message"
