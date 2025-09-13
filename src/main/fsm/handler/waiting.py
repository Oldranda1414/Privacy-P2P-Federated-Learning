from typing import Callable, Awaitable
from asyncio import sleep
from datetime import datetime

from fsm.state import State
from fsm.context import Context
from communication.message import MessageType
from peers import Peer

def get_waiting_handler(context: Context) -> Callable[[], Awaitable[State]]:
    context.comm.register_message_handler(MessageType.SYNC, _get_message_handler(context))
    async def waiting_handler() -> State:
        await context.comm.broadcast_message(MessageType.SYNC, "I am done!")
        while len(context.sync_peers) < len(context.peers):
            context.log.info(f"waiting for {len(context.peers) - len(context.sync_peers)} peers to be ready")
            await sleep(5)
        context.sync_peers = set()
        return State.SECURE_AVERAGE_COMPUTATION
    return waiting_handler

def _get_message_handler(context: Context):
    async def message_handler(sender: Peer, _content: str, _timestamp: datetime):
        context.log.info(f"Got SYNC from {sender}")
        context.sync_peers.add(sender)

    return message_handler

