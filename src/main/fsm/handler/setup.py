from asyncio import create_task, sleep
from typing import Callable, Awaitable
from datetime import datetime

from fsm.state import State
from fsm.context import Context

from communication.message import MessageType
from communication.encodable import Encodable

from machine_learning.weights import Weights
from machine_learning.dataset import get_dataset

from peers import Peer

def get_setup_handler(context: Context) -> Callable[[], Awaitable[State]]:
    context.comm.register_message_handler(MessageType.INITIAL_WEIGHTS, _get_message_handler(context))
    async def setup_handler() -> State:
        _start_heartbeat_service(context)
        _load_dataset(context)
        await _exchange_initial_weights(context)
        return State.TRAINING
    return setup_handler

def _get_message_handler(context: Context):
    async def message_handler(_sender: Peer, content: str | Encodable, _timestamp: datetime):
        if isinstance(content, Weights):
            context.model.set_weights(content)
            context.log.info("received initial weights")
        else:
            raise ValueError("initial weights received are not compatible")
    return message_handler

def _start_heartbeat_service(context: Context):
    context.heartbeat_task = create_task(context.heartbeat_service.run())

async def _exchange_initial_weights(context: Context):
    if context.owner.node_id == "node1":
        context.model.initialize()
        initial_weights = context.model.get_weights() 
        try:
            await context.comm.broadcast_message(MessageType.INITIAL_WEIGHTS, initial_weights)
        except Exception as e:
            context.log.error(f"error occured when sending weights: {e}")
        context.log.info("sent initial weights")
    else:
        while not context.model.is_initialized():
            context.log.info("waiting for initial weights")
            await sleep(5)

def _load_dataset(context: Context):
    context.dataset = get_dataset(context.owner)
