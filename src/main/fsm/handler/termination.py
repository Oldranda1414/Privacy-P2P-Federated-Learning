from typing import Callable, Awaitable
from datetime import datetime
from enum import Enum

from fsm.context import Context
from fsm.state import State
from fsm.handler.waiting import wait_for_sync

from communication.message import MessageType
from peers import Peer

# TODO check if this is a good value
ACCURACY_THRESHOLD = 0.88
MAX_ROUNDS = 15

class TerminationVote(Enum):
    IN_FAVOR = "in_favor"
    AGAINST = "against"

def get_termination_handler(context: Context) -> Callable[[], Awaitable[State]]:
    context.comm.register_message_handler(MessageType.TERMINATION, _get_message_handler(context))
    async def termination_handler() -> State:
        vote: TerminationVote | None = None
        if _training_complete(context):
            vote = TerminationVote.IN_FAVOR
        else:
            vote = TerminationVote.AGAINST
        await context.comm.broadcast_message(MessageType.TERMINATION, str(vote))
        context.termination_votes.append(vote)

        await wait_for_sync(context.termination_votes, len(context.peers) + 1, context.log, "TERMINATION VOTES")
        if TerminationVote.AGAINST in context.termination_votes:
            return State.TRAINING
        else:
            return State.SAVING_MODEL
    return termination_handler

def _get_message_handler(context: Context):
    async def message_handler(sender: Peer, content: str, _timestamp: datetime):
        context.log.info(f"Got termination vote from {sender}: {content}")
        vote = TerminationVote(content)
        context.termination_votes.append(vote)
    return message_handler

def _training_complete(context: Context) -> bool:
    if context.training_history:
        context.rounds_done += 1
        current_accuracy = context.training_history.validation_accuracy[-1]
        context.log.info(f"accuracy obtained: {current_accuracy}")
        if current_accuracy >= ACCURACY_THRESHOLD:
            return True
        elif context.rounds_done >= MAX_ROUNDS:
            return True

    return False

