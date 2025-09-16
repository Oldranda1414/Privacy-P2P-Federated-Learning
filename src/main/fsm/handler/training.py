from typing import Callable, Awaitable
from datetime import datetime

from fsm.state import State
from fsm.context import Context
from fsm.handler.waiting import wait_for_sync

from communication.message import MessageType
from peers import Peer

def get_training_handler(context: Context) -> Callable[[], Awaitable[State]]:
    context.comm.register_message_handler(MessageType.SYNC, _get_message_handler(context))
    async def training_handler() -> State:
        if context.dataset:
            context.log.info(f"training...")
            try: 
                context.training_history = context.model.train(context.dataset)
            except Exception as e:
                context.log.error(f"error occurred during training step: {e}")
                raise e
            await context.comm.broadcast_message(MessageType.SYNC, "I'm ready for SAC")
            await wait_for_sync(context.sync_peers, len(context.peers), context.log, "TRAINING")
            context.sync_peers = set()
        else:
            context.log.error("Dataset not loaded, unable to train")
        return State.SECURE_AVERAGE_COMPUTATION
    return training_handler

def _get_message_handler(context: Context):
    async def message_handler(sender: Peer, _content: str, _timestamp: datetime):
        context.log.info(f"received SYNC from {sender}")
        context.sync_peers.add(sender)

    return message_handler
